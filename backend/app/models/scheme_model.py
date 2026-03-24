from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.database import Base

class Scheme(Base):
    __tablename__ = "schemes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text)
    states = Column(JSON) # list of states like ["All", "Telangana"]
    soil_types = Column(JSON) # list of soils like ["Black", "Red"]
    water_requirement = Column(JSON) # ["Good", "Medium", "Poor"]
    recommended_crops = Column(JSON) # list of crops
    benefits = Column(Text) # text description of benefits
    official_link = Column(String)

class FarmerInput(Base):
    __tablename__ = "farmer_inputs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=True) # Optional link to user
    soil_type = Column(String)
    nitrogen = Column(Float)
    phosphorus = Column(Float)
    potassium = Column(Float)
    ph_level = Column(Float)
    land_size = Column(Float) # in acres
    water_availability = Column(String)
    location_state = Column(String)
    location_district = Column(String)

class RecommendationResult(Base):
    __tablename__ = "recommendation_results"

    id = Column(Integer, primary_key=True, index=True)
    farmer_input_id = Column(Integer, ForeignKey("farmer_inputs.id"))
    recommended_schemes = Column(JSON) # list of scheme names
    recommended_crops = Column(JSON) # list of crop names
    entrepreneur_opportunities = Column(JSON) # list of opportunities
    
    farmer_input = relationship("FarmerInput")
