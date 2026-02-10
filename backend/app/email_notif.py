from datetime import date
from sqlalchemy.orm import Session
from .models import VehicleDocument, User
from .emailService import send_email

def send_consolidated_alerts(db: Session, users: list, today: date, update_notified_flag=False):
    """
    Core logic to find expiring documents and send one email per user.
    """
    # 1. Fetch all documents
    documents = db.query(VehicleDocument).all()
    print(f"DEBUG: Found {len(documents)} total documents in DB")
    
    # Identify expiring docs
    expiring_items = []
    for doc in documents:
        days_left = (doc.expiry_date - today).days
        print(f"DEBUG: Doc {doc.id} | Days Left: {days_left} | Last Notified: {doc.last_notified_at}")
        
        if 0 <= days_left <= doc.reminder_start_days:
            # If update_notified_flag is True, check if already notified
            if not update_notified_flag or doc.last_notified_at != today:
                expiring_items.append({"doc": doc, "days": days_left})

    print(f"DEBUG: Total items to email: {len(expiring_items)}")
    
    if not expiring_items:
        return

    # 2. Build the Email for each user
    for user in users:
        table_rows = ""
        for item in expiring_items:
            d = item['doc']
            v = d.vehicle
            vehicle_info = f"{v.vehicle_type} - {v.registration_number}"
            
            table_rows += f"""
            <tr style="border-bottom: 1px solid #eee;">
                <td style="padding: 10px; font-size: 13px;"><strong>{vehicle_info}</strong></td>
                <td style="padding: 10px; font-size: 13px;">{d.document_type}</td>
                <td style="padding: 10px; font-size: 13px; color: #e53e3e;">{d.expiry_date}</td>
                <td style="padding: 10px; font-size: 13px; font-weight: bold;">{item['days']}d</td>
            </tr>
            """

        subject = f"Urgent: {len(expiring_items)} Vehicle Documents Expiring Soon"
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
        
        try:
            print(f"Sending summary to {user.email}")
            send_email(to=user.email, subject=subject, body=body)
        except Exception as e:
            print(f"Failed to send email to {user.email}: {e}")

    # 3. Update 'last_notified_at' only during the daily scheduler run
    if update_notified_flag:
        for item in expiring_items:
            item['doc'].last_notified_at = today
        db.commit()