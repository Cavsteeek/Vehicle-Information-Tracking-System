import os
from dotenv import load_dotenv
from passlib.context import CryptContext
from jose import jwt
from datetime import UTC, datetime, timedelta

load_dotenv()

# JWT config
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRY = int(os.getenv("TOKEN_EXPIRY"))

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# Hash plain password
def hash_password(password: str):
    return pwd_context.hash(password)

# Verify password during login
def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

# Create JWT token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRY
    )
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

# Decode token (used in dependencies)
def decode_token(token: str):
    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )
