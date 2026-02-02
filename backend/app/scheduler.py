from apscheduler.schedulers.background import BackgroundScheduler
from datetime import date
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import VehicleDocument, User
from .emailService import send_email

scheduler = BackgroundScheduler()

def check_document_expiries():
    """
    Runs daily.
    Checks all vehicle documents.
    Sends reminder emails to ALL registered users.
    """
    db: Session = SessionLocal()
    today = date.today()

    documents = db.query(VehicleDocument).all()
    users = db.query(User).all()  # get all registered users

    for doc in documents:
        days_left = (doc.expiry_date - today).days

        if days_left < 0:
            continue

        if days_left <= doc.reminder_start_days:
            subject = f"{doc.document_type} Expiry Reminder"
            body = f"""
Hello,

This is a reminder that a vehicle document is nearing expiry.

Document: {doc.document_type}
Expiry Date: {doc.expiry_date}
Days Remaining: {days_left}

Please ensure renewal before the expiry date.

— Vehicle Monitoring System
"""

            # Send email to every registered user
            for user in users:
                send_email(
                    to=user.email,
                    subject=subject,
                    body=body
                )

    db.close()

scheduler.add_job(check_document_expiries, "interval", days=1)
scheduler.start()
