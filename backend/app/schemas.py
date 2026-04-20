from pydantic import BaseModel, field_validator
from datetime import date, datetime
from typing import List, Optional

# ===================== AUTH =====================

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str = "logistics"  # Default role for registration

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    role: str

# ===================== VESSELS =====================

class VesselCreate(BaseModel):
    name: str
    description: Optional[str] = None

class VesselResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    documents: List[VesselDocumentResponse]

    class Config:
        from_attributes = True

class VesselDocumentCreate(BaseModel):
    title: str
    expiry_date: date
    issued_date: Optional[date] = None
    reminder_start_days: int = 21

class VesselDocumentResponse(BaseModel):
    id: int
    title: str
    expiry_date: date
    issued_date: Optional[date] = None
    status: str
    last_updated_by: Optional[str] = None
    last_updated_at: datetime

    class Config:
        from_attributes = True

# ===================== VEHICLES =====================

class VehicleDocumentCreate(BaseModel):
    document_type: str
    expiry_date: date
    reminder_start_days: int = 21


class VehicleCreate(BaseModel):
    registration_number: str
    type: str
    owner: str
    purchase_date: Optional[date] = None
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
    purchase_date: Optional[date] = None
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

