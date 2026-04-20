import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import json

load_dotenv()

def send_email(to, subject, body):
    brevo_api_key = os.getenv("BREVO_API_KEY")
    
    if brevo_api_key:
        # Use Brevo
        sender_email = os.getenv("EMAIL_USER")
        
        print(f"DEBUG: Attempting Brevo API delivery to {to}")

        url = "https://api.brevo.com/v3/smtp/email"
        
        # Brevo API Payload
        payload = {
            "sender": {"email": sender_email, "name": "Vehicle Monitor"},
            "to": [{"email": to}],
            "subject": subject,
            "htmlContent": body
        }

        headers = {
            "accept": "application/json",
            "api-key": brevo_api_key,
            "content-type": "application/json"
        }

        try:
            # Port 443 (HTTPS) is open on Render, so this won't be blocked
            response = requests.post(url, headers=headers, json=payload, timeout=20)
            
            if response.status_code in [200, 201, 202]:
                print(f"DEBUG: Brevo SUCCESS to {to}")
            else:
                print(f"ERROR: Brevo returned {response.status_code}: {response.text}")
                # This will help us see if Brevo is rejecting the "To" address
                raise Exception(f"Brevo Error: {response.text}")
                
        except Exception as e:
            print(f"CRITICAL: Failed to connect to Brevo API: {e}")
            raise e
    else:
        # Fallback to Gmail
        EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
        EMAIL_PORT = int(os.getenv("EMAIL_PORT", 465))
        EMAIL_USER = os.getenv("EMAIL_USER")
        EMAIL_PASS = os.getenv("EMAIL_PASS")

        msg = MIMEMultipart()
        msg["From"] = EMAIL_USER
        msg["To"] = to
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "html"))

        try:
            server = smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT, timeout=50)
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, to, msg.as_string())
            server.quit()
            print(f"DEBUG: Email successfully sent to {to} via Gmail")
        except Exception as e:
            print(f"ERROR in emailService: {e}")
            raise e