from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    name: str  # Renamed from full_name
    email: EmailStr
    phone: str  # Required for farmer signup
    state: str
    district: str
    role: str = "farmer"

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class GoogleLoginRequest(BaseModel):
    credential: str

class OtpRequest(BaseModel):
    phone: str

class OtpVerify(BaseModel):
    phone: str
    otp: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None

class User(UserBase):
    user_id: int
    is_active: bool
    phone_verified: bool
    created_at: datetime
    
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: User

class TokenData(BaseModel):
    email: Optional[str] = None

# Land Detail Schemas
class LandDetailBase(BaseModel):
    land_size: float
    soil_type: str
    water_availability: str
    primary_crop: str
    district: str
    village: str

class LandDetailCreate(LandDetailBase):
    pass

class LandDetailResponse(LandDetailBase):
    land_id: int
    user_id: int

    class Config:
        orm_mode = True
