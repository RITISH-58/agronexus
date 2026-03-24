"""
Upgraded Pydantic schemas for Buyer Finder and Success Stories.
"""
from pydantic import BaseModel
from typing import List, Optional

# --- BUYER SCHEMAS ---
class BuyerBase(BaseModel):
    buyer_name: str
    business_type: str
    product_category: str
    annual_capacity: Optional[str] = None
    city: str
    district: Optional[str] = None
    state: str
    latitude: float
    longitude: float
    phone_number: str
    email: str
    website: Optional[str] = None
    buyer_description: Optional[str] = None

class BuyerResponse(BuyerBase):
    id: int
    distance_km: Optional[float] = None

    class Config:
        orm_mode = True

class BuyerListResponse(BaseModel):
    buyers: List[BuyerResponse]
    total: int
    page: int = 1
    per_page: int = 50

# --- SUCCESS STORY SCHEMAS ---
class SuccessStoryResponse(BaseModel):
    id: int
    farmer_name: str
    state: str
    district: Optional[str] = None
    crop: str
    business_type: str
    investment: str
    monthly_income: str
    yearly_income: str
    products_sold: List[str] = []
    buyers_connected: List[str] = []
    government_scheme_used: Optional[str] = None
    implementation_steps: List[str] = []
    story: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None

    class Config:
        orm_mode = True

class SuccessStoryListResponse(BaseModel):
    stories: List[SuccessStoryResponse]
    total: int
    page: int = 1
    per_page: int = 20
