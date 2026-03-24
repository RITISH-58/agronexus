import numpy as np
import random
from datetime import datetime, timedelta
from typing import Optional

def generate_price_decision(crop_type: str, rainfall_deviation: float = 0.0, user_base_price: Optional[float] = None) -> dict:
    """
    AI-powered agricultural price decision system (Simulated Prophet + XGBoost).
    
    1. Fetches historical Mandi prices, arrival volumes, Weather, Sowing Data, MSP, Global Prices (Simulated).
    2. Processes features: Price trends, arrival change, rainfall dev, sowing YoY.
    3. Predicts 120-day prices and confidence score.
    4. Calculates risk score.
    5. Generates HOLD / SELL / SELL_PARTIAL decision.
    """
    crop_lower = crop_type.lower().strip()
    
    # Base real-world MSP / Mandi defaults
    base_prices = {
        "rice": 2200, "wheat": 2275, "maize": 1962, "cotton": 6620,
        "sugarcane": 315, "soybean": 4600, "groundnut": 5550,
        "tomato": 2500, "onion": 2800, "potato": 1200,
    }
    
    base_price = user_base_price if user_base_price is not None else base_prices.get(crop_lower, 3000)
    
    # --- 1. & 2. Data Processing & Features (Simulated) ---
    # We use a randomized seed based on crop to keep it consistent but dynamic
    seed = sum(ord(c) for c in crop_lower) + datetime.now().day
    rng = np.random.default_rng(seed)
    
    volatility = rng.uniform(0.05, 0.25)
    arrival_change = rng.uniform(-15.0, 20.0) # Percentage change in market arrivals
    sowing_area_change = rng.uniform(-5.0, 10.0) # YoY sowing
    
    # ─── 3. Predict future prices (120 days) via simulated ML ───
    # Prophet baseline + XGBoost external feature adjustment
    # Adjustment factor based on supply/demand features:
    # Less supply (arrivals down, sowing down) or bad weather (heavy rainfall deviation) -> Price UP
    supply_factor = (arrival_change + sowing_area_change) / 100.0
    weather_factor = abs(rainfall_deviation) / 1000.0 
    
    price_drift = rng.uniform(0.02, 0.15) - supply_factor + weather_factor
    
    # 120 days forecast calculation
    predicted_mean = base_price * (1 + price_drift)
    range_margin = predicted_mean * volatility
    
    price_min = max(base_price * 0.7, predicted_mean - range_margin)
    price_max = predicted_mean + range_margin
    confidence_score = round(rng.uniform(75.5, 94.2), 1)
    
    # ─── 4. Calculate Risk Score (0-100) ───
    # High arrival + High sowing + Low price drift -> High risk of price crash
    # High volatility -> High risk
    risk_score_raw = (volatility * 200) + (supply_factor * 100)
    risk_score = min(max(int(risk_score_raw), 15), 85) # Cap between 15 and 85
    
    # Risk Reasons
    reasons = []
    if volatility > 0.15:
        reasons.append(f"High historical price volatility ({round(volatility*100)}%)")
    if arrival_change > 5:
        reasons.append(f"Market arrivals increased by {round(arrival_change)}% (Supply pressure)")
    if sowing_area_change > 3:
        reasons.append(f"YoY Sowing area up by {round(sowing_area_change)}%")
    if rainfall_deviation < -20:
        reasons.append("Rainfall deficit may affect later harvests")
    
    if not reasons:
        reasons.append("Stable market indicators with normal supply flow.")
        
    # ─── 5. Generate Decision ───
    expected_increase = (predicted_mean - base_price) / base_price
    
    if expected_increase > 0.08 and risk_score < 60:
        decision = "HOLD"
        reasoning = f"Expected price surge of {round(expected_increase*100)}%. Risk is manageable."
    elif expected_increase < 0.02 or risk_score > 70:
        decision = "SELL"
        reasoning = f"High risk of price crash. Better to liquidate inventory."
    else:
        decision = "SELL_PARTIAL"
        reasoning = "Moderate upside expected. Liquidate 50% to cover costs & hold rest."

    return {
        "current_price": round(base_price),
        "forecast_120d": {
            "min": round(price_min),
            "max": round(price_max),
            "expected": round(predicted_mean)
        },
        "confidence_percent": confidence_score,
        "risk_score": risk_score,
        "risk_reasons": reasons,
        "recommendation": decision,
        "recommendation_reasonId": reasoning,
        # Exact Feature debugging / extra info required by UI
        "features": {
            "arrival_volumes": f"{round(arrival_change, 1)}%",
            "sowing_data": f"{round(sowing_area_change, 1)}%",
            "volatility": f"{round(volatility * 100, 1)}%",
            "msp_base": round(base_price),
            "rainfall_dev": f"{round(rainfall_deviation, 1)} mm",
            "global_commodity": "Stable"
        }
    }
