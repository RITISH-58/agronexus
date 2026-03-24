from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas import crop_schema
from app.schemas import crop_plan as plan_schema
from app.models.user import User
from app.core import security
from app.services.crop_service import CropService
import logging

# Ensure models are created
from app.models.crop_plan import CropPlan
from app.db.database import engine
from app.models.user import Base
Base.metadata.create_all(bind=engine)

router = APIRouter(tags=["Crops and Entrepreneurship"])
logger = logging.getLogger(__name__)

def get_crop_service(db: Session = Depends(get_db)):
    return CropService(db)

@router.post("/crop-recommendation", response_model=crop_schema.CropRecommendationResponse)
def get_crop_recommendation(
    request: crop_schema.CropRecommendationRequest,
    service: CropService = Depends(get_crop_service)
):
    """
    Recommend crops based on soil test results, NPK, and water.
    """
    try:
        response_data = service.get_crop_recommendations(request)
        return response_data
    except Exception as e:
        logger.error(f"Error in crop recommendation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching crop recommendations."
        )

@router.post("/agro-entrepreneur-opportunities", response_model=crop_schema.AgroEntrepreneurResponse)
def get_agro_entrepreneur_opportunities(
    request: crop_schema.AgroEntrepreneurRequest,
    service: CropService = Depends(get_crop_service)
):
    """
    Return value-added business opportunities based on recommended crops.
    """
    try:
        response_data = service.get_entrepreneur_opportunities(request)
        return response_data
    except Exception as e:
        logger.error(f"Error fetching entrepreneur opportunities: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching entrepreneur opportunities."
        )

@router.post("/crop-plans")
def create_new_crop_plan(
    plan_data: plan_schema.CropPlanCreate,
    current_user: User = Depends(security.get_current_user),
    service: CropService = Depends(get_crop_service)
):
    """
    Store a farmer's crop plan.
    """
    try:
        new_plan = service.create_crop_plan(plan_data, current_user.user_id)
        return {"message": "Crop plan created successfully", "plan_id": new_plan.plan_id}
    except Exception as e:
        logger.error(f"Error creating crop plan: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the crop plan."
        )

@router.get("/crop-dashboard/{plan_id}")
def get_crop_dashboard_view(
    plan_id: int,
    current_user: User = Depends(security.get_current_user),
    service: CropService = Depends(get_crop_service)
):
    """
    Aggregates Weather, Pest Risk, Fertilizer, Yield Prediction, and Risk Reduction logic.
    """
    try:
        return service.get_crop_dashboard(plan_id, current_user.user_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error fetching crop dashboard: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred building the intelligence dashboard."
        )

from pydantic import BaseModel, Field
from typing import Optional

class YieldPredictRequest(BaseModel):
    crop_type: str = Field(..., description="Crop name e.g. Rice, Wheat, Cotton")
    soil_type: str = Field(default="Loamy")
    rainfall_mm: float = Field(default=800.0, ge=0)
    temperature_c: float = Field(default=28.0)
    humidity: float = Field(default=65.0, ge=0, le=100)
    soil_N: float = Field(default=80.0, ge=0)
    soil_P: float = Field(default=40.0, ge=0)
    soil_K: float = Field(default=40.0, ge=0)
    soil_pH: float = Field(default=6.5, ge=0, le=14)
    area: float = Field(default=1.0, ge=0.1, description="Land area in acres")

@router.post("/predict-yield")
def predict_yield_direct(
    request: YieldPredictRequest,
    service: CropService = Depends(get_crop_service)
):
    """
    Standalone ML yield prediction endpoint.
    Accepts crop, soil, and weather parameters → returns predicted yield,
    confidence score, optimal scenario, and AI recommendations.
    """
    try:
        result = service.predict_yield_standalone(request.model_dump())
        return result
    except Exception as e:
        logger.error(f"Error in yield prediction: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Yield prediction failed. Please try again."
        )

