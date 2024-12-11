import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import hashlib
from datetime import datetime, timedelta

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password, hashed_password):
    return hash_password(plain_password) == hashed_password

def send_otp_email(email, otp):
    # Configure these with your email settings
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "your-email@gmail.com"
    sender_password = "your-app-specific-password"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = email
    message["Subject"] = "Your TransformoDocs Verification Code"

    body = f"""
    Welcome to TransformoDocs!
    
    Your verification code is: {otp}
    
    This code will expire in 10 minutes.
    """
    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def is_otp_valid(otp_created_at):
    if not otp_created_at:
        return False
    return datetime.utcnow() - otp_created_at < timedelta(minutes=10)