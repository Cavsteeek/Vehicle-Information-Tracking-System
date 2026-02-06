import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import date, datetime
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import User
from .email_notif import send_consolidated_alerts

scheduler = BackgroundScheduler()

def check_document_expiries():
    print("Scheduler running at", date.today())
    db: Session = SessionLocal()
    try:
        users = db.query(User).all()
        # Pass ALL users and set update_notified_flag=True
        send_consolidated_alerts(db, users, date.today(), update_notified_flag=True)
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
            # seconds=10,  # seconds for testing
            id="document_expiry_job",
            replace_existing=True,
            max_instances=1,
            next_run_time=datetime.now()  # Start immediately for testing
        )
        scheduler.start()
        print("Scheduler started")
