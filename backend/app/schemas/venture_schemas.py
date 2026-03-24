"""
Pydantic schemas for the Smart Agri Venture Planner.
"""
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

# --- REQUEST SCHEMAS ---
class VentureRecommendRequest(BaseModel):
    soil_type: Optional[str] = None
    land_size: Optional[float] = None  # acres
    season: Optional[str] = None
    water_availability: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    budget: Optional[str] = None  # e.g., "3-5"
    business_type: Optional[str] = None
    search_query: Optional[str] = None  # free-text product search

# --- RESPONSE SCHEMAS ---
class VentureCardResponse(BaseModel):
    id: int
    crop_name: str
    venture_name: str
    business_category: str
    demand_level: str
    investment_range: str
    roi_range: str
    monthly_income: str
    profit_margin: str
    image_url: Optional[str] = None

    class Config:
        orm_mode = True

class VentureListResponse(BaseModel):
    ventures: List[VentureCardResponse]
    total: int

class VentureDetailResponse(BaseModel):
    id: int
    crop_name: str
    venture_name: str
    business_category: str
    demand_level: str
    investment_range: str
    roi_range: str
    monthly_income: str
    profit_margin: str
    soil_suitability: str
    water_requirement: str
    season_suitability: str
    image_url: Optional[str] = None
    raw_material_required: Dict[str, Any] = {}
    machinery_required: List[str] = []
    production_capacity: Dict[str, Any] = {}
    market_demand: Dict[str, Any] = {}
    investment_breakdown: Dict[str, Any] = {}
    implementation_steps: List[str] = []

    class Config:
        orm_mode = True
