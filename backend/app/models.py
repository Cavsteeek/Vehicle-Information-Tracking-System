from sqlalchemy import (
    Column, Integer, String, Date, DateTime,
    ForeignKey, Text
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

# ===================== USERS =====================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)

# ===================== VEHICLES =====================

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    registration_number = Column(String, unique=True, index=True)
    type = Column(String)
    owner = Column(String)
    purchase_date = Column(Date)
    remark = Column(String, nullable=True)

    # One vehicle → many documents
    documents = relationship(
        "VehicleDocument",
        back_populates="vehicle",
        cascade="all, delete"
    )

# ===================== VEHICLE DOCUMENTS =====================

class VehicleDocument(Base):
    __tablename__ = "vehicle_documents"

    id = Column(Integer, primary_key=True, index=True)

    # Foreign key to vehicle
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))

    document_type = Column(String)
    expiry_date = Column(Date)

    # Reminder config
    reminder_start_days = Column(Integer, default=21)
    last_notified_at = Column(Date, nullable=True)

    # Business status
    status = Column(String, default="ACTIVE")

    # Non-repudiation
    last_updated_by = Column(String)
    last_updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )

    vehicle = relationship("Vehicle", back_populates="documents")

# ===================== AUDIT LOG =====================

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)

    # What was changed
    entity_type = Column(String, index=True)
    entity_id = Column(Integer, index=True)

    # CREATE / RENEW / UPDATE
    action = Column(String)

    # Who did it
    performed_by = Column(String)

    # When (DB time)
    performed_at = Column(DateTime, server_default=func.now())

    # Before + after snapshot (JSON as string)
    old_value = Column(Text, nullable=True)
    new_value = Column(Text, nullable=True)
