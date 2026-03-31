from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import jwt
import bcrypt

from database.db import get_db
from models.user import User

from fastapi import Header
from jose import JWTError

router = APIRouter()

# JWT configuration
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# Request model for user registration
class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str


# Request model for user login
class LoginRequest(BaseModel):
    email: str
    password: str


# Register new user
@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password
    hashed_password = bcrypt.hashpw(
        data.password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    # Create new user
    new_user = User(
        name=data.name,
        email=data.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}


# Login user and generate JWT token
@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    # Get user by email
    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Verify password
    if not bcrypt.checkpw(
        data.password.encode("utf-8"),
        user.password.encode("utf-8")
    ):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Set token expiration time
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": user.email,
        "exp": expire
    }

    # Create JWT token
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": token,
        "token_type": "bearer"
    }


def verify_token(authorization: str = Header(None)):

    if not authorization:
        raise HTTPException(status_code=401, detail="Token missing")

    try:
        scheme, token = authorization.split()

        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme")

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
@router.get("/profile")
def profile(payload: dict = Depends(verify_token)):
    return {
        "message": "Access granted",
        "user": payload["sub"]
    }