import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import date, datetime
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
            print(f"Checking Doc: {doc.document_type} | Expiry: {doc.expiry_date} | Start Days: {doc.reminder_start_days}")
            
            days_left = (doc.expiry_date - today).days
            print(f"Days left calculated: {days_left}")

            if days_left < 0:
                print(f"Skipping {doc.document_type}: Already expired.")
                continue

            if days_left <= doc.reminder_start_days:
                if doc.last_notified_at == today:
                    continue  # Skip sending email if already notified today
                
                subject = f"Action Required: {doc.document_type} Expiry"

                for user in users:
                    body = f"""
    <html>
    <body style="font-family: sans-serif; color: #333; line-height: 1.6;">
        <div style="max-width: 600px; margin: 0 auto; border: 1px solid #eee; border-radius: 10px; overflow: hidden;">
            <div style="background-color: #000; color: #fff; padding: 20px; text-align: center;">
                <h1 style="margin: 0; font-size: 20px;">Vehicle Document Alert</h1>
            </div>
            <div style="padding: 20px;">
                <p>Hello <strong>{user.name}</strong>,</p>
                <p>This is a reminder that a vehicle document is nearing its expiry date.</p>
                
                <div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <p style="margin: 5px 0;"><strong>Document:</strong> {doc.document_type}</p>
                    <p style="margin: 5px 0;"><strong>Expiry Date:</strong> <span style="color: #e53e3e;">{doc.expiry_date}</span></p>
                    <p style="margin: 5px 0;"><strong>Days Remaining:</strong> {days_left}</p>
                </div>

                <p style="font-size: 14px; color: #666;">
                    Please ensure this is renewed before the deadline to avoid penalties.
                </p>
            </div>
            <div style="background-color: #f4f4f4; padding: 10px; text-align: center; font-size: 12px; color: #999;">
                &copy; 2026 Vehicle Particulars Monitoring System
            </div>
        </div>
    </body>
    </html>
    """
                    print(f"Sending email to {user.email}")
                    send_email(
                        to=user.email,
                        subject=subject,
                        body=body
                    )
                doc.last_notified_at = today
                db.commit()


    except Exception as e:
        print("Scheduler error:", e)

    finally:
        db.close()

def start_scheduler():
    if not scheduler.running:
        scheduler.add_job(
            check_document_expiries,
            trigger="interval",
            days=1,  # days for prod
            # hours = 12,
            # seconds=10,  # seconds for testing
            id="document_expiry_job",
            replace_existing=True,
            max_instances=1,
            next_run_time=datetime.now()  # Start immediately for testing
        )
        scheduler.start()
        print("Scheduler started")
