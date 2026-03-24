from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.db.database import Base

class LandDetail(Base):
    __tablename__ = "land_details"

    land_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    land_size = Column(Float)
    soil_type = Column(String)
    water_availability = Column(String)
    primary_crop = Column(String)
    district = Column(String)
    village = Column(String)
