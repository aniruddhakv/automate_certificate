import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os

class EmailSender:
    def __init__(self, smtp_server, smtp_port):
        """
        Initialize email sender
        
        Args:
            smtp_server (str): SMTP server address
            smtp_port (int): SMTP server port
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
    
    def send_certificate(self, sender_email, sender_password, recipient_email, 
                        certificate_path, subject="Your Certificate", 
                        body="Please find your certificate attached."):
        """
        Send certificate via email
        
        Args:
            sender_email (str): Sender's email address
            sender_password (str): Sender's email password
            recipient_email (str): Recipient's email address
            certificate_path (str): Path to certificate file
            subject (str): Email subject
            body (str): Email body text
        """
        # Create message container
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        
        # Add body text
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach certificate
        with open(certificate_path, 'rb') as f:
            img = MIMEImage(f.read())
            img.add_header('Content-Disposition', 'attachment', 
                         filename=os.path.basename(certificate_path))
            msg.attach(img)
        
        # Send email
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
