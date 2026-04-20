from fastapi import APIRouter, Body, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import UserCreate, Token, UserLogin, UserResponse
from ..auth import hash_password, verify_password, create_access_token
from ..deps import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if db_user.role not in ["logistics", "vessel", "admin", "multi_dept"]:
        raise HTTPException(status_code=403, detail="Account not authorized. Please contact administrator.")

    access_token = create_access_token(
        data={"sub": db_user.email, "role": db_user.role}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": db_user.role
    }

@router.get("/users", response_model=List[UserResponse])
def list_users(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    # Admin-only
    db_user = db.query(User).filter(User.email == current_user).first()
    if not db_user or db_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can list users")
    return db.query(User).all()

@router.post("/users/create", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    # Admin-only endpoint to create users
    db_admin = db.query(User).filter(User.email == current_user).first()
    if not db_admin or db_admin.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can create users")
    
    # Validate role
    if user.role not in ["logistics", "vessel", "admin", "multi_dept"]:
        raise HTTPException(status_code=400, detail="Invalid role. Must be: logistics, vessel, admin, or multi_dept")
    
    # Check if user already exists
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user with specified role
    new_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hash_password(user.password),
        role=user.role
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.put("/users/{user_id}/role")
def update_user_role(user_id: int, role: str = Body(...), db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_admin = db.query(User).filter(User.email == current_user).first()
    if not db_admin or db_admin.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can update roles")

    if role not in ["logistics", "vessel", "admin", "multi_dept"]:
        raise HTTPException(status_code=400, detail="Invalid role")

    user_to_update = db.query(User).filter(User.id == user_id).first()
    if not user_to_update:
        raise HTTPException(status_code=404, detail="User not found")

    user_to_update.role = role
    db.add(user_to_update)
    db.commit()
    db.refresh(user_to_update)

    return {"message": "Role updated", "user": {
        "id": user_to_update.id,
        "email": user_to_update.email,
        "role": user_to_update.role
    }}

@router.get("/me")
def get_current_user_info(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role
    }
