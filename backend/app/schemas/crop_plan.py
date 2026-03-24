from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class CropPlanBase(BaseModel):
    crop_type: str
    soil_type: str
    season: str
    land_acres: float
    water_source: str
    location: str
    sowing_date: str
    
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
