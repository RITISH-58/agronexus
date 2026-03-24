from pydantic import BaseModel, Field
from typing import List, Optional

class SchemeRecommendationRequest(BaseModel):
    soil_type: str = Field(..., description="Type of soil (e.g., Alluvial, Black, Red)")
    land_size: float = Field(..., description="Size of land in acres")
    water_availability: str = Field(..., description="Water availability (e.g., Good, Medium, Poor)")
    state: str = Field(..., description="State where the land is located")
    district: str = Field(..., description="District where the land is located")

class RecommendedScheme(BaseModel):
    name: str
    benefit: str
    link: Optional[str] = None

class SchemeRecommendationResponse(BaseModel):
    recommended_schemes: List[RecommendedScheme]
