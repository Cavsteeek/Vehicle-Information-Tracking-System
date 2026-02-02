import os
import bcrypt  # Use this instead of passlib
from dotenv import load_dotenv
from jose import jwt
from datetime import UTC, datetime, timedelta

load_dotenv()

# JWT config
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
# Use a default value in case .env fails to load
ACCESS_TOKEN_EXPIRY = int(os.getenv("TOKEN_EXPIRY", 1440)) 

# --- REPLACED PASSLIB WITH BCRYPT ---

def hash_password(password: str) -> str:
    # 1. Convert string to bytes
    pwd_bytes = password.encode('utf-8')
    # 2. Generate salt and hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    # 3. Return as string for database storage
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Convert both to bytes and compare
    return bcrypt.checkpw(
        plain_password.encode('utf-8'), 
        hashed_password.encode('utf-8')
    )

# --- JWT LOGIC (Corrected with UTC) ---

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRY)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])