from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Vehicle, VehicleDocument, AuditLog
from ..schemas import DocumentRenewRequest, VehicleCreate
from ..deps import get_current_user
import json

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/whoami")
def whoami(current_user: str = Depends(get_current_user)):
    return {"email": current_user}


@router.post("/")
def create_vehicle(
    vehicle: VehicleCreate,
    db: Session = Depends(get_db),
    user_email: str = Depends(get_current_user)
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

    for doc in vehicle.documents:
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
    return {"message": "Vehicle created"}

@router.put("/documents/{doc_id}")
def update_document(
    doc_id: int,
    payload: DocumentRenewRequest,
    db: Session = Depends(get_db),
    user_email: str = Depends(get_current_user)
):
    doc = db.query(VehicleDocument).filter_by(id=doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    old_value = {
        "expiry_date": str(doc.expiry_date),
        "status": doc.status
    }

    doc.expiry_date = payload.new_expiry_date
    doc.status = "ACTIVE"
    doc.last_updated_by = user_email

    db.add(AuditLog(
        entity_type="DOCUMENT",
        entity_id=doc.id,
        action="RENEW",
        performed_by=user_email,
        old_value=json.dumps(old_value),
        new_value=json.dumps({"expiry_date": str(payload.new_expiry_date)})
    ))

    db.commit()
    return {"message": "Document updated"}
