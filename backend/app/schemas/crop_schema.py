from pydantic import BaseModel, Field
from typing import List, Optional

class CropRecommendationRequest(BaseModel):
    soil_type: str = Field(..., description="Type of soil (e.g., Alluvial, Black, Red)")
    nitrogen: float = Field(..., description="Nitrogen content in soil")
    phosphorus: float = Field(..., description="Phosphorus content in soil")
    potassium: float = Field(..., description="Potassium content in soil")
    ph_level: float = Field(..., description="pH level of soil")
    water_availability: str = Field(..., description="Water availability (e.g., Good, Medium, Poor)")
    state: str = Field(..., description="State where the land is located")

class RecommendedCrop(BaseModel):
    crop_name: str
    suitability_score: float

class CropRecommendationResponse(BaseModel):
    recommended_crops: List[RecommendedCrop]

class AgroEntrepreneurRequest(BaseModel):
    recommended_crops: List[str] = Field(..., description="List of recommended crops to find business opportunities for")

class BusinessOpportunity(BaseModel):
    crop: str
    business_opportunity: str
    processing_idea: str
    expected_profit_potential: str

class AgroEntrepreneurResponse(BaseModel):
    entrepreneur_opportunities: List[BusinessOpportunity]
