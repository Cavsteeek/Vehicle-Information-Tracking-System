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
        # Dictionary to hold documents grouped by user: { user_obj: [doc1, doc2] }
        user_alerts = {}

        # 1. Fetch all documents and their associated vehicles/owners
        # Using join(Vehicle) to ensure we know who the owner is if needed
        documents = db.query(VehicleDocument).all()
        users = db.query(User).all()

        for doc in documents:
            days_left = (doc.expiry_date - today).days
            
            # Logic: If it's expiring soon and hasn't been notified today
            if 0 <= days_left <= doc.reminder_start_days:
                if doc.last_notified_at != today:
                    # We add this doc to the list for every user
                    for user in users:
                        if user not in user_alerts:
                            user_alerts[user] = []
                        user_alerts[user].append({"doc": doc, "days": days_left})

        # 2. Send one email per user containing all their alerts
        for user, alerts in user_alerts.items():
            if not alerts:
                continue

            # Build the HTML table rows for the documents
            table_rows = ""
            for item in alerts:
                d = item['doc']
                v = d.vehicle  # Access the related vehicle
                days = item['days']
                
                # Format: White Hilux - RUM106XB
                vehicle_info = f"{v.vehicle_type} - {v.registration_number}"
                
                table_rows += f"""
                <tr style="border-bottom: 1px solid #eee;">
                    <td style="padding: 10px; font-size: 13px;"><strong>{vehicle_info}</strong></td>
                    <td style="padding: 10px; font-size: 13px;">{d.document_type}</td>
                    <td style="padding: 10px; font-size: 13px; color: #e53e3e;">{d.expiry_date}</td>
                    <td style="padding: 10px; font-size: 13px; font-weight: bold;">{days}d</td>
                </tr>
                """

            subject = f"Urgent: {len(alerts)} Vehicle Documents Expiring Soon"
            body = f"""
            <html>
            <body style="font-family: sans-serif; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; border: 1px solid #000; border-radius: 10px; overflow: hidden;">
                    <div style="background-color: #000; color: #fff; padding: 20px; text-align: center;">
                        <h1 style="margin: 0; font-size: 20px;">Document Expiry Summary</h1>
                    </div>
                    <div style="padding: 20px;">
                        <p>Hello <strong>{user.name}</strong>,</p>
                        <p>The following documents in your fleet require attention:</p>
                        
                        <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                            <thead>
                               <tr style="background-color: #f4f4f4; text-align: left;">
                                    <th style="padding: 10px; font-size: 12px;">Vehicle</th>
                                    <th style="padding: 10px; font-size: 12px;">Document</th>
                                    <th style="padding: 10px; font-size: 12px;">Expiry</th>
                                    <th style="padding: 10px; font-size: 12px;">Left</th>
                                </tr>
                            </thead>
                            <tbody>
                                {table_rows}
                            </tbody>
                        </table>

                        <p style="font-size: 13px; color: #666;">After renewal, please log in to the portal to update these records.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            print(f"Sending summary email to {user.email}")
            send_email(to=user.email, subject=subject, body=body)

            # 3. Mark all these documents as notified today
            for item in alerts:
                item['doc'].last_notified_at = today
        
        db.commit()

    except Exception as e:
        print("Scheduler error:", e)
        db.rollback()
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
