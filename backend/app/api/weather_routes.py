from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any

from app.ml.weather_service import (
    get_current_weather, get_weather_forecast, generate_weather_alerts, is_india_location
)
from app.ml.pest_prediction import predict_pest_risk
from app.ml.disease_risk import predict_disease_risk
from app.ml.irrigation_advisor import get_irrigation_advice
from app.ml.farming_advisor import get_farming_advice
from app.services.hazard_detection import detect_hazards

router = APIRouter()

# --- Request Schemas ---
class PestRiskRequest(BaseModel):
    crop: str
    temperature: float
    humidity: int
    rainfall_mm: Optional[float] = 0.0

class DiseaseRiskRequest(BaseModel):
    crop: str
    temperature: float
    humidity: int
    rainfall_mm: Optional[float] = 0.0
    cloud_coverage: Optional[int] = 50

class IrrigationAdviceRequest(BaseModel):
    crop: str
    temperature: float
    humidity: int
    rain_forecast_mm: float
    recent_rainfall_mm: Optional[float] = 0.0

class FarmingAdviceRequest(BaseModel):
    crop: str
    soil_type: str
    weather_conditions: Dict[str, Any]


def _validate_india(location: str):
    if not is_india_location(location):
        raise HTTPException(
            status_code=400,
            detail="Weather monitoring is available for India locations only."
        )


# --- Endpoints ---
@router.get("/weather/current")
def read_current_weather(location: str = "Hyderabad"):
    """Returns current weather data for an India location."""
    _validate_india(location)
    return get_current_weather(location)


@router.get("/weather/forecast")
def read_weather_forecast(location: str = "Hyderabad", days: int = 7):
    """Returns a multi-day weather forecast."""
    _validate_india(location)
    return get_weather_forecast(location, days)


@router.get("/weather/alerts")
def read_weather_alerts(location: str = "Hyderabad"):
    """Generates weather alerts based on the upcoming forecast."""
    _validate_india(location)
    forecast = get_weather_forecast(location, 7)
    alerts = generate_weather_alerts(forecast)
    return {"alerts": alerts}


@router.get("/weather/hazards")
def read_weather_hazards(location: str = "Hyderabad"):
    """Returns composite hazard assessment for an India location."""
    _validate_india(location)
    weather = get_current_weather(location)
    forecast = get_weather_forecast(location, 7)
    hazards = detect_hazards(weather, forecast)
    return {"hazards": hazards, "location": location}


@router.post("/weather/pest-risk")
def calculate_pest_risk(request: PestRiskRequest):
    """Calculates pest risk based on crop and environmental conditions."""
    return predict_pest_risk(
        crop=request.crop,
        temperature=request.temperature,
        humidity=request.humidity,
        rainfall_mm=request.rainfall_mm
    )


@router.post("/weather/disease-risk")
def calculate_disease_risk(request: DiseaseRiskRequest):
    """Predicts crop disease risk from weather conditions."""
    return predict_disease_risk(
        crop=request.crop,
        temperature=request.temperature,
        humidity=request.humidity,
        rainfall_mm=request.rainfall_mm,
        cloud_coverage=request.cloud_coverage
    )


@router.post("/weather/irrigation-advice")
def calculate_irrigation_advice(request: IrrigationAdviceRequest):
    """Generates smart irrigation recommendations."""
    return get_irrigation_advice(
        crop=request.crop,
        temperature=request.temperature,
        humidity=request.humidity,
        rain_forecast_mm=request.rain_forecast_mm,
        recent_rainfall_mm=request.recent_rainfall_mm
    )


# Keep legacy aliases for backward compat with Dashboard
@router.post("/pest-risk")
def legacy_pest_risk(request: PestRiskRequest):
    return predict_pest_risk(
        crop=request.crop,
        temperature=request.temperature,
        humidity=request.humidity,
        rainfall_mm=request.rainfall_mm
    )

@router.post("/farming-advice")
def generate_farming_advice(request: FarmingAdviceRequest):
    """Generates AI farming advice based on crop, soil, and weather."""
    return get_farming_advice(
        crop=request.crop,
        soil_type=request.soil_type,
        weather_conditions=request.weather_conditions
    )
