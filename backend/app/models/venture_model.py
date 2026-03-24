"""
SQLAlchemy model for the Agri Venture Dataset.
"""
from sqlalchemy import Column, Integer, String, Text, Float
from app.db.database import Base

class AgriVentureDataset(Base):
    __tablename__ = "agri_venture_dataset"

    id = Column(Integer, primary_key=True, index=True)
    crop_name = Column(String, index=True)           # e.g., Rice, Milk, Turmeric
    venture_name = Column(String, index=True)          # e.g., Puffed Rice Manufacturing
    business_category = Column(String, index=True)     # e.g., Crop Processing, Dairy
    soil_suitability = Column(String)                  # CSV: "Alluvial,Loamy,Black Soil"
    water_requirement = Column(String)                 # Low / Medium / High
    season_suitability = Column(String)                # CSV: "Kharif,Rabi,Summer"
    investment_range = Column(String)                  # e.g., "₹3-5 Lakhs"
    investment_min = Column(Float)                     # numeric for filtering (in lakhs)
    investment_max = Column(Float)
    roi_range = Column(String)                         # e.g., "25-35%"
    monthly_income = Column(String)                    # e.g., "₹60,000 - ₹80,000"
    profit_margin = Column(String)                     # e.g., "30-40%"
    demand_level = Column(String)                      # Very High / High / Medium
    raw_material_required = Column(Text)               # JSON
    machinery_required = Column(Text)                  # JSON list
    production_capacity = Column(Text)                 # JSON
    market_demand = Column(Text)                       # JSON (buyers list)
    investment_breakdown = Column(Text)                # JSON
    implementation_steps = Column(Text)                # JSON list
    image_url = Column(String)                         # Unsplash/Pexels URL
