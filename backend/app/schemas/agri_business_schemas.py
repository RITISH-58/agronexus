"""
Pydantic schemas for the Business Blueprint system.
"""
from pydantic import BaseModel
from typing import List, Dict, Optional, Any


class SchemeModel(BaseModel):
    name: str
    benefit: str
    link: str

class MarketDemandModel(BaseModel):
    Level: str
    Buyers: List[str]
    Cities: List[str]
    Growth: str

class AgriBusinessBase(BaseModel):
    business_name: str
    crop_type: str
    category: str
    investment: str
    roi: str
    revenue_range: str
    profit_margin: str
    break_even: str
    market_demand_level: str

class AgriBusinessDetail(AgriBusinessBase):
    id: int
    investment_breakdown: Dict[str, str]
    production_capacity: Dict[str, str]
    revenue_projection: Dict[str, str]
    market_demand: MarketDemandModel
    machinery: List[str]
    skills_required: List[str]
    schemes: List[SchemeModel]
    implementation_steps: List[str]

    class Config:
        orm_mode = True

class AgriBusinessListResponse(BaseModel):
    businesses: List[AgriBusinessDetail]
    total: int
