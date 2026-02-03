# from apscheduler.schedulers.background import BackgroundScheduler
# from datetime import date
# from sqlalchemy.orm import Session
# from .database import SessionLocal
# from .models import VehicleDocument, User
# from .emailService import send_email

# scheduler = BackgroundScheduler()

# def check_document_expiries():
#     print("Scheduler running at", date.today())

#     """
#     Runs daily.
#     Checks all vehicle documents.
#     Sends reminder emails to ALL registered users.
#     """
#     db: Session = SessionLocal()
#     today = date.today()

#     documents = db.query(VehicleDocument).all()
#     users = db.query(User).all()  # get all registered users

#     for doc in documents:
#         days_left = (doc.expiry_date - today).days

#         if days_left < 0:
#             continue

#         if days_left <= doc.reminder_start_days:
#             users = db.query(User).all()  # get all registered users
#             subject = f"{doc.document_type} Expiry Reminder"
#             body = f"""
# Hello,

# This is a reminder that a vehicle document is nearing expiry.

# Document: {doc.document_type}
# Expiry Date: {doc.expiry_date}
# Days Remaining: {days_left}

# Please ensure renewal before the expiry date.
# """

#             # Send email to every registered user
#             for user in users:
#                 send_email(
#                     to=user.email,
#                     subject=subject,
#                     body=body
#                 )

#     db.close()

# def start_scheduler():
#     if not scheduler.running:
#         scheduler.add_job(
#             check_document_expiries,
#             trigger="interval",
#             # days=1,
#             seconds=10,
#             id="document_expiry_job",
#             replace_existing=True
#         )
#         scheduler.start()
#         print("Scheduler started")


from apscheduler.schedulers.background import BackgroundScheduler
from datetime import date
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import VehicleDocument, User
from .emailService import send_email

scheduler = BackgroundScheduler()

def check_document_expiries():
    print("Scheduler running at", date.today())

    db: Session = SessionLocal()
    today = date.today()

    try:
        documents = db.query(VehicleDocument).all()
        users = db.query(User).all()

        for doc in documents:
            days_left = (doc.expiry_date - today).days

            if days_left < 0:
                continue

            if days_left <= doc.reminder_start_days:
                if doc.last_notified_at == today:
                    continue  # Skip sending email if already notified today
                doc.last_notified_at = today
                db.commit()

                subject = f"{doc.document_type} Expiry Reminder"

                for user in users:
                    body = f"""
Hello {user.name},

This is a reminder that a vehicle document is nearing expiry.

Document: {doc.document_type}
Expiry Date: {doc.expiry_date}
Days Remaining: {days_left}

Please ensure renewal before the expiry date.
"""
                    print(f"Sending email to {user.email}")
                    send_email(
                        to=user.email,
                        subject=subject,
                        body=body
                    )

    except Exception as e:
        print("Scheduler error:", e)

    finally:
        db.close()

def start_scheduler():
    if not scheduler.running:
        scheduler.add_job(
            check_document_expiries,
            trigger="interval",
            days=1,  # seconds for testing, days for prod
            id="document_expiry_job",
            replace_existing=True,
            max_instances=1
        )
        scheduler.start()
        print("Scheduler started")
