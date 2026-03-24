"""
SQLAlchemy models for the Blueprint System.
"""
from sqlalchemy import Column, Integer, String, Text
from app.db.database import Base


class AgriBusiness(Base):
    __tablename__ = "agri_business"

    id = Column(Integer, primary_key=True, index=True)
    business_name = Column(String, index=True)
    crop_type = Column(String, index=True)
    category = Column(String, index=True)  # food_processing, oil_extraction, etc.
    investment = Column(String)  # e.g. "₹6-10 Lakhs"
    roi = Column(String)  # e.g. "30-40%"
    revenue_range = Column(String)  # e.g. "₹2.5-4 Lakhs"
    profit_margin = Column(String)  # e.g. "22-28%"
    break_even = Column(String)  # e.g. "12-16 Months"
    
    # JSON strings
    investment_breakdown = Column(Text)
    production_capacity = Column(Text)
    revenue_projection = Column(Text)
    market_demand_level = Column(String) # Very High, High, Medium
    market_demand = Column(Text) # JSON: {"Buyers": [], "Cities": [], "Growth": ""}
    machinery = Column(Text)  # JSON list
    skills_required = Column(Text)  # JSON list
    schemes = Column(Text)  # JSON list of dicts: {"name", "benefit", "link"}
    implementation_steps = Column(Text)  # JSON list of strings
