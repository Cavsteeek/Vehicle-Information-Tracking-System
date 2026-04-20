from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from ..database import get_db
from ..models import Vessel, VesselDocument, AuditLog
from ..schemas import (
    VesselCreate, VesselResponse,
    VesselDocumentCreate, VesselDocumentResponse,
    DocumentRenewRequest
)
from ..deps import get_current_user, require_roles
import json
from datetime import date

router = APIRouter(prefix="/vessel-docs", tags=["Vessel Docs"])


@router.get("/vessels", response_model=List[VesselResponse])
def get_all_vessels(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
    role: str = Depends(require_roles("vessel", "admin", "multi_dept"))
):
    return db.query(Vessel).options(joinedload(Vessel.documents)).all()


@router.post("/vessels")
def create_vessel(
    payload: VesselCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
    role: str = Depends(require_roles("vessel", "admin", "multi_dept"))
):
    existing = db.query(Vessel).filter(Vessel.name == payload.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Vessel already exists")

    vessel = Vessel(name=payload.name, description=payload.description)
    db.add(vessel)
    db.commit()
    db.refresh(vessel)

    db.add(AuditLog(
        entity_type="VESSEL",
        entity_id=vessel.id,
        action="CREATE",
        performed_by=current_user,
        new_value=json.dumps(payload.dict(), default=str)
    ))
    db.commit()

    return {"message": "Vessel created"}


@router.get("/", response_model=List[VesselDocumentResponse])
def get_all_vessel_docs(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
    role: str = Depends(require_roles("vessel", "admin", "multi_dept"))
):
    docs = db.query(VesselDocument).all()
    return [
        {
            **doc.__dict__,
            "status": "EXPIRED" if (doc.expiry_date - date.today()).days < 0 else (
                "ACTIVE" if (doc.expiry_date - date.today()).days > doc.reminder_start_days else f"{(doc.expiry_date - date.today()).days} days left"
            )
        }
        for doc in docs
    ]


@router.post("/")
def create_vessel_doc(
    payload: VesselDocumentCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
    role: str = Depends(require_roles("vessel", "admin", "multi_dept"))
):
    # Ensure at least one vessel exists.
    vessel = db.query(Vessel).first()
    if not vessel:
        vessel = Vessel(name="Default Vessel", description="Auto created vessel")
        db.add(vessel)
        db.flush()

    doc = VesselDocument(
        vessel_id=vessel.id,
        title=payload.title,
        expiry_date=payload.expiry_date,
        issued_date=payload.issued_date,
        reminder_start_days=payload.reminder_start_days,
        last_updated_by=current_user
    )
    db.add(doc)
    db.flush()

    db.add(AuditLog(
        entity_type="VESSEL_DOCUMENT",
        entity_id=doc.id,
        action="CREATE",
        performed_by=current_user,
        new_value=json.dumps(payload.dict(), default=str)
    ))

    db.commit()

    return {"message": "Vessel document created"}


@router.put("/{doc_id}")
def update_vessel_doc(
    doc_id: int,
    payload: DocumentRenewRequest,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
    role: str = Depends(require_roles("vessel", "admin", "multi_dept"))
):
    doc = db.query(VesselDocument).filter_by(id=doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Vessel document not found")

    old_value = {"expiry_date": str(doc.expiry_date)}
    doc.expiry_date = payload.new_expiry_date
    doc.last_updated_by = current_user

    db.add(AuditLog(
        entity_type="VESSEL_DOCUMENT",
        entity_id=doc.id,
        action="RENEW",
        performed_by=current_user,
        old_value=json.dumps(old_value),
        new_value=json.dumps({"expiry_date": str(payload.new_expiry_date)})
    ))

    db.commit()
    return {"message": "Vessel document updated"}


@router.delete("/{doc_id}")
def delete_vessel_doc(
    doc_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
    role: str = Depends(require_roles("vessel", "admin", "multi_dept"))
):
    doc = db.query(VesselDocument).filter_by(id=doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Vessel document not found")

    db.delete(doc)
    db.commit()

    return {"message": "Vessel document deleted"}
