from apscheduler.schedulers.background import BackgroundScheduler
from datetime import date
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import VehicleDocument
from .emailService import send_email

scheduler = BackgroundScheduler()

def check_document_expiries():
    db: Session = SessionLocal()
    today = date.today()

    documents = db.query(VehicleDocument).all()

    for doc in documents:
        days_left = (doc.expiry_date - today).days

        if days_left < 0:
            continue

        if days_left <= doc.reminder_start_days:
            subject = f"{doc.document_type} Expiry Reminder"
            body = f"""
Hello,

Reminder that your vehicle document is nearing expiry.

Document: {doc.document_type}
Expiry Date: {doc.expiry_date}
Days Remaining: {days_left}

Please renew before expiry.
"""

            send_email(
                to="your_email_here@gmail.com",
                subject=subject,
                body=body
            )

    db.close()

scheduler.add_job(check_document_expiries, "interval", days=1)
scheduler.start()
