# import smtplib
# import os
# from email.message import EmailMessage
# from dotenv import load_dotenv
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

# load_dotenv()

# EMAIL_HOST = os.getenv("EMAIL_HOST")
# EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
# EMAIL_USER = os.getenv("EMAIL_USER")
# EMAIL_PASS = os.getenv("EMAIL_PASS")

# def send_email(to, subject, body):

#     msg = MIMEMultipart()
#     msg["From"] = EMAIL_USER
#     msg["To"] = to
#     msg["Subject"] = subject

#     msg.attach(MIMEText(body, "html"))

#     try:
#         with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT, timeout=15) as server:
#             server.login(EMAIL_USER, EMAIL_PASS)
#             server.sendmail(EMAIL_USER, to, msg.as_string())
#         print(f"DEBUG: Email successfully sent to {to}")
#     except Exception as e:
#         print(f"ERROR in emailService: {e}")
#         raise e


import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# load_dotenv() // for local testing

# Use .get() with defaults to prevent crashes
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587)) # Switch to 587 for better cloud compatibility
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

def send_email(to, subject, body):
    print(f"DEBUG: Attempting to connect to {EMAIL_HOST}:{EMAIL_PORT}...")
    
    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = to
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))

    try:
        # Use SMTP + starttls (Standard for Port 587)
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT, timeout=15)
        server.set_debuglevel(1)
        server.starttls() # Secure the connection
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, to, msg.as_string())
        server.quit()
        print(f"DEBUG: Email SUCCESS to {to}")
    except Exception as e:
        print(f"ERROR in emailService: {e}")
        raise e