from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class CropPlan(Base):
    __tablename__ = "crop_plans"

    plan_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    
    # Core Plan Attributes
    crop_type = Column(String, index=True)
    soil_type = Column(String)
    season = Column(String)  # Kharif / Rabi / Summer
    land_acres = Column(Float) # in Acres
    water_source = Column(String) # Low / Medium / High
    location = Column(String) # District or Region string
    sowing_date = Column(String) # YYYY-MM-DD
    
    # Optional Specific Variables useful for precise ML
    nitrogen_level = Column(Float, nullable=True)
    phosphorus_level = Column(Float, nullable=True)
    potassium_level = Column(Float, nullable=True)
    soil_ph = Column(Float, nullable=True)
    base_price = Column(Float, nullable=True)
    
    # Store weather fetched once at plan creation
    temperature = Column(Float, nullable=False, default=28.0)
    humidity = Column(Float, nullable=False, default=65.0)
    rainfall = Column(Float, nullable=False, default=800.0)
    wind_speed = Column(Float, nullable=False, default=12.0)
    
    # Farmer-Friendly Observations
    water_retention = Column(String, nullable=True)
    soil_texture = Column(String, nullable=True)
    cracking_behavior = Column(String, nullable=True)
    water_req = Column(String, nullable=True)
    crop_perf = Column(String, nullable=True)
    soil_color = Column(String, nullable=True)
    rain_behavior = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # Allow mapping back to the User model if needed
    owner = relationship("User")
