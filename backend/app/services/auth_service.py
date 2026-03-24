from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from google.oauth2 import id_token
from google.auth.transport import requests
import random
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash
from app.core.config import settings

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    password_hash = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        name=user.name,
        phone=user.phone,
        state=user.state,
        district=user.district,
        role=user.role,
        password_hash=password_hash
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def verify_google_token(token: str):
    try:
        # Request Google to verify the token
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), settings.GOOGLE_CLIENT_ID)
        return idinfo
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Google token",
        )

# Mock OTP store (in production use Redis or DB table)
otp_store = {}

def send_otp_sms(phone: str, otp: str):
    # In production, use your preferred SMS provider.
    # We are mocking the OTP sending process here.
    print(f"MOCK OTP for {phone}: {otp}")

def generate_and_send_otp(phone: str):
    otp = str(random.randint(100000, 999999))
    otp_store[phone] = otp
    # Send via SMS service
    send_otp_sms(phone, otp)
    return True

def verify_and_clear_otp(phone: str, otp: str):
    if otp == "123456": # Bypass for testing
        return True
        
    if phone in otp_store and otp_store[phone] == otp:
        del otp_store[phone]
        return True
    return False
