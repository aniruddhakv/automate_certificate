from PIL import Image, ImageDraw, ImageFont
import os

class CertificateGenerator:
    def __init__(self, template_path, font_path, font_size=15):
        self.template = Image.open(template_path)
        self.font = ImageFont.truetype(font_path, font_size)

    def create_certificate(self, name, output_path, position=(1284, 903)):
        """Create a certificate for a participant"""
        # Create a copy of the template
        certificate = self.template.copy()
        draw = ImageDraw.Draw(certificate)
        
        # Calculate text size using textbbox instead of textsize
        bbox = draw.textbbox((0, 0), name, font=self.font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Calculate center position
        x = position[0] - text_width // 2
        y = position[1] - text_height // 2
        
        # Add name to certificate
        draw.text((x, y), name, fill='white', font=self.font)
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save the certificate
        certificate.save(output_path)
        return output_path
