from pydantic import BaseModel, Field
from typing import List, Optional

# --- Entrepreneur Mode: Crop-based opportunities ---
class EntrepreneurModeRequest(BaseModel):
    crop: str = Field(..., description="Crop name (e.g. rice, maize, turmeric)")

class BusinessOpportunityItem(BaseModel):
    name: str
    investment: str
    investment_numeric: Optional[int] = None
    roi: str
    market_demand: str
    trending: Optional[bool] = False
    description: str
    machinery: Optional[List[str]] = None
    government_schemes: Optional[List[str]] = None
    production_process: Optional[str] = None
    raw_materials: Optional[str] = None
    monthly_revenue: Optional[str] = None
    profit_margin: Optional[str] = None
    breakeven: Optional[str] = None
    export_potential: Optional[str] = None

class EntrepreneurModeResponse(BaseModel):
    crop: str
    business_opportunities: List[BusinessOpportunityItem]

# --- Trending Businesses ---
class TrendingBusinessesResponse(BaseModel):
    trending_businesses: List[BusinessOpportunityItem]

# --- Search ---
class SearchRequest(BaseModel):
    query: str = Field(..., description="Search term (e.g. 'oil', 'food processing')")
    investment_filter: Optional[str] = Field(None, description="low (<5L), medium (5-20L), high (>20L)")
    demand_filter: Optional[str] = Field(None, description="High, Very High, Medium")

class SearchResponse(BaseModel):
    results: List[BusinessOpportunityItem]
    total: int

# --- Business Plan ---
class BusinessPlanRequest(BaseModel):
    business_name: str = Field(..., description="Name of the business to generate a plan for")

class SchemeSupport(BaseModel):
    name: str
    benefit: str
    official_link: str

class BusinessPlanResponse(BaseModel):
    business_name: str
    crop: str
    introduction: str
    market_opportunity: str
    required_machinery: List[str]
    raw_material_sources: str
    manufacturing_process: str
    investment_breakdown: str
    operational_costs: str
    expected_revenue: str
    profit_margin: str
    breakeven_period: str
    export_potential: str
    government_schemes: List[SchemeSupport]
    startup_roadmap: List[str]
