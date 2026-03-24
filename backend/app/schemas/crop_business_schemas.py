from pydantic import BaseModel
from typing import List, Dict, Optional, Any

# Section details
class InvestmentBreakdownDetails(BaseModel):
    machinery: str
    setup: str
    packaging: str
    working_capital: str
    total: str

class RawMaterialDetails(BaseModel):
    daily_crop_req: str
    processing_yield: str

class ProductionCapacityDetails(BaseModel):
    daily_output: str
    monthly_production: str

class RevenueProjectionDetails(BaseModel):
    selling_price: str
    monthly_revenue: str
    monthly_expenses: str
    estimated_profit: str

class MarketDemandDetails(BaseModel):
    demand_level: str
    buyers: List[str]
    cities: List[str]

# Main Schema for response
class CropBusinessResponse(BaseModel):
    id: int
    crop_name: str
    processed_product: str
    industry_type: str
    demand_level: str
    industry_growth_rate: str
    
    investment_range: str
    roi_range: str
    monthly_revenue: str
    profit_margin: str
    break_even: str
    
    investment_breakdown: InvestmentBreakdownDetails
    raw_material_req: RawMaterialDetails
    production_capacity: ProductionCapacityDetails
    revenue_projection: RevenueProjectionDetails
    market_demand: MarketDemandDetails
    
    machinery: List[str]
    skills_required: List[str]
    schemes: List[str]
    implementation_steps: List[str]

    class Config:
        orm_mode = True

class CropBusinessListResponse(BaseModel):
    businesses: List[CropBusinessResponse]
