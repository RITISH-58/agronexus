from pydantic import BaseModel, validator
from typing import Any

VALID_CROPS = ["rice", "cotton", "groundnut", "maize", "wheat", "sugarcane", "tomato", "potato"]

class CropIntelRequest(BaseModel):
    crop: str
    previous_crop: str
    land_size: float = 1.0
    
    @validator("crop")
    def validate_crop(cls, value):
        return value.lower().strip()

    @validator("previous_crop", pre=True, always=True)
    def validate_prev_crop(cls, value):
        if not value:
            return "rice"
        val = value.lower().strip()
        if val not in VALID_CROPS:
            return "rice"
        return val

class SoilProfile(BaseModel):
    type: str
    N: Any
    P: Any
    K: Any
    pH: Any

class CropIntelResponse(BaseModel):
    yield_per_acre: str
    total_harvest: str
    market_price: str
    trend: str
    forecast: str
    soil_profile: SoilProfile
    confidence: str
