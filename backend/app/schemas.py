from pydantic import BaseModel
from datetime import date, datetime
from typing import List, Optional

# ===================== AUTH =====================

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

# ===================== VEHICLES =====================

class VehicleDocumentCreate(BaseModel):
    document_type: str
    expiry_date: date
    reminder_start_days: int = 21


class VehicleCreate(BaseModel):
    registration_number: str
    type: str
    owner: str
    purchase_date: date
    remark: Optional[str] = None
    documents: List[VehicleDocumentCreate]


class VehicleDocumentResponse(BaseModel):
    id: int
    document_type: str
    expiry_date: date
    status: str
    last_updated_by: Optional[str] = None
    last_updated_at: datetime

    class Config:
        from_attributes = True


class VehicleResponse(BaseModel):
    id: int
    registration_number: str
    vehicle_type: str
    owner: str
    purchase_date: date
    documents: List[VehicleDocumentResponse]

    class Config:
        from_attributes = True
        
class DocumentRenewRequest(BaseModel):
    new_expiry_date: date

# ===================== AUDIT =====================

class AuditLogResponse(BaseModel):
    id: int
    entity_type: str
    entity_id: int
    action: str
    performed_by: str
    performed_at: str
    old_value: Optional[str]
    new_value: Optional[str]

    class Config:
        from_attributes = True
