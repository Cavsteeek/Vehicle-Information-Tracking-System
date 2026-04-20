from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, Vehicle, VehicleDocument, AuditLog
from ..schemas import DocumentRenewRequest, VehicleCreate, VehicleResponse
from ..deps import get_current_user, require_roles
import json
from datetime import date
from ..email_notif import send_consolidated_alerts

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])

@router.get("/whoami")
def whoami(current_user: str = Depends(get_current_user), role: str = Depends(require_roles("logistics", "admin", "multi_dept"))):
    return {"email": current_user, "role": role}

# Get all vehicles
@router.get("/", response_model=List[VehicleResponse])
def get_all_vehicles(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
    role: str = Depends(require_roles("logistics", "admin", "multi_dept"))
):
    """Fetch all vehicles and their associated documents."""
    vehicles = db.query(Vehicle).all()
    return vehicles

# Get single vehicle
@router.get("/{vehicle_id}", response_model=VehicleResponse)
def get_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
    role: str = Depends(require_roles("logistics", "admin", "multi_dept"))
):
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle

# delete Vehicle
@router.delete("/{vehicle_id}")
def delete_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
    role: str = Depends(require_roles("logistics", "admin", "multi_dept"))
):
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    db.delete(vehicle)
    db.commit()
    return {"message": f"Vehicle {vehicle_id} and its documents deleted successfully"}

# Create new vehicle
@router.post("/")
def create_vehicle(
    vehicle: VehicleCreate,
    db: Session = Depends(get_db),
    user_email: str = Depends(get_current_user),
    role: str = Depends(require_roles("logistics", "admin", "multi_dept"))
):
    db_vehicle = Vehicle(
        registration_number=vehicle.registration_number,
        vehicle_type=vehicle.type,
        owner=vehicle.owner,
        purchase_date=vehicle.purchase_date,
        remark=vehicle.remark
    )

    db.add(db_vehicle)
    db.flush()  # get vehicle.id
    
    has_urgent_doc = False
    for doc in vehicle.documents:
        days_left = (doc.expiry_date - date.today()).days
        if days_left <= doc.reminder_start_days:
            has_urgent_doc = True
        db_doc = VehicleDocument(
            vehicle_id=db_vehicle.id,
            document_type=doc.document_type,
            expiry_date=doc.expiry_date,
            reminder_start_days=doc.reminder_start_days,
            last_updated_by=user_email
        )
        db.add(db_doc)

    db.add(AuditLog(
        entity_type="VEHICLE",
        entity_id=db_vehicle.id,
        action="CREATE",
        performed_by=user_email,
        new_value=json.dumps(vehicle.dict(), default=str)
    ))

    db.commit()
    if has_urgent_doc:
        try:
            # Send instant alert to all users for urgent vehicle documents
            all_users = db.query(User).all()
            if all_users:
                print(f"DEBUG: Triggering instant alert for new urgent vehicle.")
                send_consolidated_alerts(db, all_users, date.today(), update_notified_flag=False)
        except Exception as e:
            print(f"DEBUG: Instant notification failed: {e}")
    
    return {"message": "Vehicle created"}

@router.put("/documents/{doc_id}")
def update_document(
    doc_id: int,
    payload: DocumentRenewRequest,
    db: Session = Depends(get_db),
    user_email: str = Depends(get_current_user),
    role: str = Depends(require_roles("logistics", "admin", "multi_dept"))
):
    doc = db.query(VehicleDocument).filter_by(id=doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    old_value = {
        "expiry_date": str(doc.expiry_date)
    }

    doc.expiry_date = payload.new_expiry_date
    doc.last_updated_by = user_email

    db.add(AuditLog(
        entity_type="VEHICLE_DOCUMENT",
        entity_id=doc.id,
        action="RENEW",
        performed_by=user_email,
        old_value=json.dumps(old_value),
        new_value=json.dumps({"expiry_date": str(payload.new_expiry_date)})
    ))

    db.commit()
    return {"message": "Document updated"}
