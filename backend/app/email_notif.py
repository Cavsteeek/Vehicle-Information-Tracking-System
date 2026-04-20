from datetime import date
from sqlalchemy.orm import Session
from .models import VehicleDocument, VesselDocument, User
from .emailService import send_email


def _compute_status(doc):
    days_left = (doc.expiry_date - date.today()).days
    if days_left < 0:
        return "EXPIRED", "Expired"
    if days_left <= doc.reminder_start_days:
        return f"{days_left}d", f"{days_left} days left"
    return "ACTIVE", "Active"


def send_consolidated_alerts(db: Session, users: list, today: date, update_notified_flag=False):
    """
    Email alert for expiring/expired docs, split by truncated role.
    """
    vehicle_docs = db.query(VehicleDocument).all()
    vessel_docs = db.query(VesselDocument).all()

    vehicle_alerts = []
    for d in vehicle_docs:
        days_left = (d.expiry_date - today).days
        if days_left <= d.reminder_start_days and (not update_notified_flag or d.last_notified_at != today):
            status_code, status_label = _compute_status(d)
            vehicle_alerts.append({"doc": d, "status_label": status_label, "days_left": days_left})

    vessel_alerts = []
    for d in vessel_docs:
        days_left = (d.expiry_date - today).days
        if days_left <= d.reminder_start_days and (not update_notified_flag or d.last_notified_at != today):
            status_code, status_label = _compute_status(d)
            vessel_alerts.append({"doc": d, "status_label": status_label, "days_left": days_left})

    print(f"DEBUG: vehicle_alerts={len(vehicle_alerts)}, vessel_alerts={len(vessel_alerts)}")

    if not vehicle_alerts and not vessel_alerts:
        return

    for user in users:
        if user.role == "admin":
            relevant_vehicles = vehicle_alerts
            relevant_vessels = vessel_alerts
        elif user.role == "logistics":
            relevant_vehicles = vehicle_alerts
            relevant_vessels = []
        elif user.role == "vessel":
            relevant_vehicles = []
            relevant_vessels = vessel_alerts
        else:
            continue

        if not relevant_vehicles and not relevant_vessels:
            continue

        rows = ""

        if relevant_vehicles:
            for item in relevant_vehicles:
                d = item["doc"]
                v = d.vehicle
                vehicle_info = f"{v.vehicle_type} - {v.registration_number}"
                rows += f"""
                <tr style=\"border-bottom: 1px solid #eee;\">
                    <td style=\"padding: 10px; font-size: 13px;\"><strong>{vehicle_info}</strong></td>
                    <td style=\"padding: 10px; font-size: 13px;\">{d.document_type}</td>
                    <td style=\"padding: 10px; font-size: 13px;\">{d.expiry_date}</td>
                    <td style=\"padding: 10px; font-size: 13px; font-weight: bold;\">{item['status_label']}</td>
                </tr>
                """

        if relevant_vessels:
            for item in relevant_vessels:
                d = item["doc"]
                vessel_name = d.vessel.name if d.vessel else "Unknown"
                rows += f"""
                <tr style=\"border-bottom: 1px solid #eee;\">
                    <td style=\"padding: 10px; font-size: 13px;\"><strong>{vessel_name}</strong></td>
                    <td style=\"padding: 10px; font-size: 13px;\">{d.title}</td>
                    <td style=\"padding: 10px; font-size: 13px;\">{d.expiry_date}</td>
                    <td style=\"padding: 10px; font-size: 13px; font-weight: bold;\">{item['status_label']}</td>
                </tr>
                """

        subject = "Urgent: Document(s) Require Attention"
        body = f"""
        <html>
        <body style=\"font-family: sans-serif; color: #333;\">
            <div style=\"max-width: 600px; margin: 0 auto; border: 1px solid #000; border-radius: 10px; overflow: hidden;\">
                <div style=\"background-color: #000; color: #fff; padding: 20px; text-align: center;\">
                    <h1 style=\"margin: 0; font-size: 20px;\">Document Status Summary</h1>
                </div>
                <div style=\"padding: 20px;\">
                    <p>Hello <strong>{user.name}</strong>,</p>
                    <p>The following documents are either expired or expiring soon:</p>
                    <table style=\"width: 100%; border-collapse: collapse; margin: 20px 0;\">
                        <thead>
                            <tr style=\"background-color: #f4f4f4; text-align: left;\">
                                <th style=\"padding: 10px; font-size: 12px;\">Entity</th>
                                <th style=\"padding: 10px; font-size: 12px;\">Document</th>
                                <th style=\"padding: 10px; font-size: 12px;\">Expiry Date</th>
                                <th style=\"padding: 10px; font-size: 12px;\">Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            {rows}
                        </tbody>
                    </table>
                    <p style=\"font-size: 13px; color: #666;\">Please update these records in the portal once renewed.</p>
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

    if update_notified_flag:
        for item in vehicle_alerts:
            item["doc"].last_notified_at = today
        for item in vessel_alerts:
            item["doc"].last_notified_at = today
        db.commit()
