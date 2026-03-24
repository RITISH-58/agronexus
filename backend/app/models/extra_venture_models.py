"""
Upgraded SQLAlchemy models for Buyer Finder and Success Stories.
"""
from sqlalchemy import Column, Integer, String, Text, Float
from app.db.database import Base

class BuyerDirectory(Base):
    __tablename__ = "buyer_directory"
    
    id = Column(Integer, primary_key=True, index=True)
    buyer_name = Column(String, index=True)
    business_type = Column(String)  # e.g., Wholesale Trader, Food Processor
    product_category = Column(String, index=True)
    annual_capacity = Column(String)
    city = Column(String, index=True)
    district = Column(String)
    state = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    phone_number = Column(String)
    email = Column(String)
    website = Column(String)
    buyer_description = Column(Text)

class SuccessStory(Base):
    __tablename__ = "success_stories"
    
    id = Column(Integer, primary_key=True, index=True)
    farmer_name = Column(String, index=True)
    state = Column(String, index=True)
    district = Column(String)
    crop = Column(String, index=True)
    business_type = Column(String)
    investment = Column(String)
    monthly_income = Column(String)
    yearly_income = Column(String)
    products_sold = Column(Text)  # JSON list
    buyers_connected = Column(Text)  # JSON list
    government_scheme_used = Column(String)
    implementation_steps = Column(Text)  # JSON list
    story = Column(Text)
    contact_phone = Column(String)
    contact_email = Column(String)
