import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

# print("EMAIL CONFIG CHECK")
# print("HOST:", EMAIL_HOST)
# print("PORT:", EMAIL_PORT)
# print("USER:", EMAIL_USER)
# print("PASS SET:", EMAIL_PASS is not None)


def send_email(to: str, subject: str, body: str):
    msg = EmailMessage()
    msg["From"] = EMAIL_USER
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)
         
    with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT, timeout=10) as server:
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
