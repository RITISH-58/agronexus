from sqlalchemy import Boolean, Column, Integer, String, DateTime
from datetime import datetime
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True, index=True, nullable=True)
    password_hash = Column(String, nullable=True) # Nullable for purely Google OAuth users
    state = Column(String, nullable=True)
    district = Column(String, nullable=True)
    role = Column(String, default="farmer")
    
    google_id = Column(String, unique=True, index=True, nullable=True)
    phone_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
