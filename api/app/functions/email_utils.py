import io
import os
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


env = os.getenv('APP_ENV', 'dev')
load_dotenv(f".env.{env}")


def send_email(to_email: str, subject: str, body: str, attachment: io.BytesIO = None) -> bool:
    smtp_server = os.environ.get("SMTP_SERVER", "email-smtp.us-east-1.amazonaws.com")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    smtp_username = os.environ.get("SMTP_USERNAME")
    smtp_password = os.environ.get("SMTP_PASSWORD")
    from_email = os.environ.get("FROM_EMAIL")
    
    if not smtp_username or not smtp_password:
        print("SMTP credentials not configured")
        return False
    
    try:
        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = "estebanlopezg7@gmail.com"  # Override recipient for testing, replace with: to_email
        msg["Subject"] = subject
        
        msg.attach(MIMEText(body, "html"))

        if attachment:
            attachment.seek(0)
            file_name = f"paz_y_salvo_{to_email}.pdf"
            att = MIMEApplication(attachment.read())
            att.add_header('Content-Disposition', 'attachment', filename=file_name)
            msg.attach(att)

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
        server.quit()
        
        print(f"Email sent successfully to {to_email}")
        return True
    except Exception as e:
        print(f"Failed to send email to {to_email}: {str(e)}")
        return False


def try_send_email(email_address: str, subject: str, body: str, attachment: io.BytesIO = None, max_retries: int = 3):
    for attempt in range(1, max_retries + 1):
        print(f"Attempt {attempt} of {max_retries} to send email to {email_address}")
        success = send_email(email_address, subject, body, attachment)
        
        if success:
            return True
        
        if attempt < max_retries:
            print(f"Retry {attempt} failed, attempting again...")
    
    print(f"Failed to send email to {email_address} after {max_retries} attempts")
    return False
