from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import os
from ..emailService import send_email
from ..database import SessionLocal
from ..models import User
from ..schemas import UserCreate, Token, UserLogin
from ..auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    # 1. Check for existing user
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # 2. Create the new user
    new_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 3. ADMIN NOTIFICATION: Send email to YOU about this new registration
    try:
        admin_email = "chimdiebubeuzo@gmail.com"
        admin_subject = "Action Required: New User Registration Request"
        admin_body = f"""
        <html>
            <body style="font-family: sans-serif; color: #333;">
                <div style="padding: 20px; border: 1px solid #000; border-radius: 8px;">
                    <h2 style="color: #000;">New Access Request</h2>
                    <p>A new user has registered and is waiting for approval:</p>
                    <ul>
                        <li><strong>Name:</strong> {new_user.name}</li>
                        <li><strong>Email:</strong> {new_user.email}</li>
                    </ul>
                    <p>To grant access, add this email to your <strong>APPROVED_USERS</strong> list.</p>
                </div>
            </body>
        </html>
        """
        # Using your existing send_email function
        send_email(to=admin_email, subject=admin_subject, body=admin_body)
    except Exception as e:
        # We print the error but don't stop the registration process
        print(f"DEBUG: Admin notification failed: {e}")

    return {"message": "Registration successful. Access is pending admin approval."}

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    raw_list = os.getenv("APPROVED_USERS", "chimdiebubeuzo@gmail.com")
    APPROVED_USERS = [email.strip() for email in raw_list.split(",")]
    
    if db_user.email not in APPROVED_USERS:
        raise HTTPException(status_code=403, detail="Account pending admin approval. Please contact chimdiebubeuzo@gmail.com")

    access_token = create_access_token(
        data={"sub": db_user.email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
