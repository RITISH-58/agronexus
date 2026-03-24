from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class CropPlanBase(BaseModel):
    crop_type: str
    soil_type: Optional[str] = None
    season: str
    land_acres: float
    water_source: Optional[str] = None
    location: str
    sowing_date: str
    
    # Feature Engineering Observations
    water_retention: Optional[str] = None
    soil_texture: Optional[str] = None
    cracking_behavior: Optional[str] = None
    water_req: Optional[str] = None
    crop_perf: Optional[str] = None
    soil_color: Optional[str] = None
    rain_behavior: Optional[str] = None
    
    # Optional Specific Variables useful for precise ML
    nitrogen_level: Optional[float] = None
    phosphorus_level: Optional[float] = None
    potassium_level: Optional[float] = None
    soil_ph: Optional[float] = None
    base_price: Optional[float] = None

class CropPlanCreate(CropPlanBase):
    pass

class CropPlanResponse(CropPlanBase):
    plan_id: int
    user_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
