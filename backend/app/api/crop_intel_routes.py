from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.schemas.crop_intel import CropIntelRequest, CropIntelResponse, SoilProfile
import joblib
import os

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, 'models')

def load_model(name):
    path = os.path.join(MODELS_DIR, name)
    if not os.path.exists(path):
        return None
    return joblib.load(path)

# Load global models once to prevent thread lock
yield_model_global = load_model('yield_model.pkl')
price_model_global = load_model('price_model.pkl')
soil_model_global = load_model('soil_model.pkl')
le_crop_global = load_model('le_crop.pkl')
le_prev_global = load_model('le_prev.pkl')
le_soil_global = load_model('le_soil.pkl')

@router.post("/crop-intel", response_model=CropIntelResponse)
def get_crop_intel(request: CropIntelRequest):
    VALID_CROPS = ["rice", "cotton", "groundnut", "maize", "wheat", "sugarcane", "tomato", "potato"]
    if request.crop not in VALID_CROPS:
        return JSONResponse(status_code=400, content={
            "error": "Invalid input. Please enter a valid crop.",
            "supported_crops": VALID_CROPS
        })
        
    if not all([yield_model_global, price_model_global, soil_model_global, le_crop_global, le_prev_global, le_soil_global]):
        raise HTTPException(status_code=500, detail="Unable to process request")
        
    try:
        c_enc = le_crop_global.transform([request.crop])[0]
        p_enc = le_prev_global.transform([request.previous_crop])[0]
        
        X_input = [[c_enc, p_enc]]
        
        pred_yield = yield_model_global.predict(X_input)[0]
        pred_price = price_model_global.predict(X_input)[0]
        pred_soil_encoded = soil_model_global.predict(X_input)[0]
        
        pred_soil = le_soil_global.inverse_transform([pred_soil_encoded])[0]
        
        if pred_soil == "high_nitrogen":
            N, P, K = 80, 40, 30
            ph = 6.5
            soil_display = "High Nitrogen"
        elif pred_soil == "low_nitrogen":
            N, P, K = 30, 40, 35
            ph = 5.5
            soil_display = "Low Nitrogen"
        else: # balanced
            N, P, K = 50, 30, 30
            ph = 6.8
            soil_display = "Balanced"
            
        soil_profile = SoilProfile(
            type=soil_display, N=N, P=P, K=K, pH=ph
        )
        
        # Total harvest deterministic calculation
        total_harvest_val = pred_yield * request.land_size
        
        # Trend generation deterministic
        if request.crop in ["cotton", "groundnut"]:
            trend_str = "+7%"
            forecast_str = "Price likely to increase"
        else:
            trend_str = "+3%"
            forecast_str = "Stable market"
            
        # Confidence score mapping exactly
        common_combinations = [("cotton", "groundnut"), ("rice", "wheat"), ("maize", "potato")]
        if (request.crop, request.previous_crop) in common_combinations:
            conf_str = "87%"
        else:
            conf_str = "74%"
            
        return CropIntelResponse(
            yield_per_acre=f"{round(pred_yield, 1)} quintals",
            total_harvest=f"{round(total_harvest_val, 1)} quintals",
            market_price=f"₹{int(pred_price)}",
            trend=trend_str,
            forecast=forecast_str,
            soil_profile=soil_profile,
            confidence=conf_str
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid crop input")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unable to process request")
