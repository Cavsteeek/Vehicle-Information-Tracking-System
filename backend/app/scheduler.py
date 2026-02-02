from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Vehicle
from datetime import date

scheduler = BackgroundScheduler()

def check_expiries():
    db: Session = SessionLocal()
    today = date.today()

    vehicles = db.query(Vehicle).all()

    for v in vehicles:
        for field in [
            "insurance",
            "road_worthiness",
            "vehicle_licence"
        ]:
            expiry = getattr(v, field)
            if expiry and (expiry - today).days in [21, 14, 7, 0]:
                print(f"Reminder: {field} expires for {v.registration_number}")

    db.close()

scheduler.add_job(check_expiries, "interval", days=1)
scheduler.start()
