from sqlalchemy import Column, Integer, String, Text
from app.db.database import Base

class CropBusinessDataset(Base):
    __tablename__ = "crop_business_dataset"

    id = Column(Integer, primary_key=True, index=True)
    crop_name = Column(String, index=True) # e.g., 'Potato'
    processed_product = Column(String, index=True) # e.g., 'Potato Chips Manufacturing'
    industry_type = Column(String) # e.g., 'Food Processing'
    demand_level = Column(String) # e.g., 'Very High'
    industry_growth_rate = Column(String) # e.g., '12% Annual Growth'
    
    # Financial Numeric Highlights
    investment_range = Column(String) # e.g., '₹8–12 Lakhs'
    roi_range = Column(String) # e.g., '35–45%'
    monthly_revenue = Column(String) # e.g., '₹3–5 Lakhs'
    profit_margin = Column(String) # e.g., '25–30%'
    break_even = Column(String) # e.g., '14 Months'
    
    # JSON Fields for the 10 Detailed Blueprint Sections
    investment_breakdown = Column(Text) # JSON dict {machinery, setup, packaging, working_capital, total}
    raw_material_req = Column(Text) # JSON dict {daily_crop_req, processing_yield}
    production_capacity = Column(Text) # JSON dict {daily_output, monthly_production}
    revenue_projection = Column(Text) # JSON dict {selling_price, monthly_revenue, monthly_expenses, estimated_profit}
    market_demand = Column(Text) # JSON dict {demand_level, buyers: list, cities: list}
    machinery = Column(Text) # JSON list of strings
    skills_required = Column(Text) # JSON list of strings
    schemes = Column(Text) # JSON list of strings or dicts
    implementation_steps = Column(Text) # JSON list of strings
