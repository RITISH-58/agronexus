from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.db.database import get_db
from app.schemas import user as schemas
from app.models import user as models
from app.services import auth_service
from app.core import security
from app.core.config import settings

router = APIRouter()

@router.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = auth_service.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check phone uniqueness
    if user.phone:
        db_phone = db.query(models.User).filter(models.User.phone == user.phone).first()
        if db_phone:
            raise HTTPException(status_code=400, detail="Phone number already registered")

    new_user = auth_service.create_user(db=db, user=user)
    
    # Optional: Automatically send OTP on signup
    if new_user.phone:
        auth_service.generate_and_send_otp(new_user.phone)
        
    return {"message": "Account created successfully"}

@router.post("/login", response_model=schemas.Token)
def login(login_data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = auth_service.get_user_by_email(db, email=login_data.email)
    if not user or not user.password_hash or not security.verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "user": user}

@router.post("/google-login", response_model=schemas.Token)
def google_login(request: schemas.GoogleLoginRequest, db: Session = Depends(get_db)):
    idinfo = auth_service.verify_google_token(request.credential)
    email = idinfo['email']
    name = idinfo.get('name', 'User')
    google_id = idinfo['sub']

    user = auth_service.get_user_by_email(db, email=email)
    
    if not user:
        # Create user automatically if they don't exist
        user = models.User(
            email=email,
            name=name,
            google_id=google_id,
            phone_verified=True, # Trust Google's auth for basic verification
            password_hash=None # No password for Google oauth users
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer", "user": user}

@router.post("/send-otp")
def send_otp(request: schemas.OtpRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.phone == request.phone).first()
    if not user:
        raise HTTPException(status_code=404, detail="User with this phone number not found")
        
    auth_service.generate_and_send_otp(request.phone)
    return {"message": "OTP sent successfully"}

@router.post("/verify-otp")
def verify_otp(request: schemas.OtpVerify, db: Session = Depends(get_db)):
    is_valid = auth_service.verify_and_clear_otp(request.phone, request.otp)
    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
        
    user = db.query(models.User).filter(models.User.phone == request.phone).first()
    if user:
        user.phone_verified = True
        db.commit()
        
    return {"message": "Phone number verified successfully"}

@router.get("/me", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(security.get_current_user)):
    return current_user
