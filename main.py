from src.certificate_generator import CertificateGenerator
from src.email_sender import EmailSender
from src.utils import setup_logging, load_config
import pandas as pd
import os
from dotenv import load_dotenv

def main():
    # Setup logging
    setup_logging()
    
    # Load environment variables
    load_dotenv()
    
    # Load configuration
    config = load_config()
    
    # Initialize certificate generator
    generator = CertificateGenerator(
        template_path=config['certificate']['template_path'],
        font_path=config['certificate']['font_path'],
        font_size=config['certificate']['font_size']
    )
    
    # Initialize email sender
    email_sender = EmailSender(
        smtp_server=config['email']['smtp_server'],
        smtp_port=config['email']['smtp_port']
    )
    
    # Read participant data
    df = pd.read_excel(config['data']['participants_file'])
    
    # Create output directory if it doesn't exist
    os.makedirs(config['output']['certificates_dir'], exist_ok=True)
    
    # Process each participant
    results = {'success': [], 'failed': []}
    for _, row in df.iterrows():
        try:
            # Generate certificate
            certificate_path = os.path.join(
                config['output']['certificates_dir'],
                f"{row['Name']}_certificate.png"
            )
            
            generator.create_certificate(
                name=row['Name'],
                output_path=certificate_path,
                position=(
                    config['certificate']['position']['x'],
                    config['certificate']['position']['y']
                )
            )
            
            # Send certificate via email
            email_sender.send_certificate(
                sender_email=config['email']['sender_email'],
                sender_password=config['email']['sender_password'],
                recipient_email=row['Email'],  # Changed from receiver_email to recipient_email
                certificate_path=certificate_path
            )
            
            results['success'].append(row['Name'])
            
        except Exception as e:
            print(f"Error processing certificate for {row['Name']}: {str(e)}")
            results['failed'].append(row['Name'])
    
    # Print results
    print(f"Successfully processed: {len(results['success'])} certificates")
    print(f"Failed to process: {len(results['failed'])} certificates")

if __name__ == "__main__":
    main()
