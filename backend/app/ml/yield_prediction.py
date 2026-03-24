"""
yield_prediction.py — Production ML-Based Crop Yield Prediction
================================================================
Loads a trained RandomForestRegressor and returns:
  - predicted_yield_per_acre (quintals)
  - total_yield
  - confidence_score (0-100)
  - avg_regional_yield / optimal_yield (for chart comparison)
  - recommendations (AI-generated improvement suggestions)
"""

import os
import json
import numpy as np
import joblib
import logging

logger = logging.getLogger(__name__)

# ─── Load model artifacts at module level (once on server startup) ───
_MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")

try:
    _model        = joblib.load(os.path.join(_MODEL_DIR, "yield_model.pkl"))
    _scaler       = joblib.load(os.path.join(_MODEL_DIR, "yield_scaler.pkl"))
    _crop_encoder = joblib.load(os.path.join(_MODEL_DIR, "crop_encoder.pkl"))
    _soil_encoder = joblib.load(os.path.join(_MODEL_DIR, "soil_encoder.pkl"))
    with open(os.path.join(_MODEL_DIR, "crop_averages.json"), "r") as f:
        _crop_averages = json.load(f)
    _model_loaded = True
    logger.info("✅ Yield prediction model loaded successfully")
except Exception as e:
    _model_loaded = False
    _model = _scaler = _crop_encoder = _soil_encoder = _crop_averages = None
    logger.warning(f"⚠️ Yield model not found, please run train_models.py first: {e}")


# ─── Ideal ranges for computing optimal scenario ───
IDEAL_CONDITIONS = {
    "Rice":      {"N": 100, "P": 50, "K": 50, "pH": 6.0, "rain": 1200, "temp": 27, "hum": 80},
    "Wheat":     {"N": 120, "P": 60, "K": 40, "pH": 6.8, "rain": 550,  "temp": 18, "hum": 60},
    "Maize":     {"N": 125, "P": 60, "K": 50, "pH": 6.4, "rain": 650,  "temp": 25, "hum": 70},
    "Cotton":    {"N": 80,  "P": 40, "K": 30, "pH": 6.8, "rain": 800,  "temp": 30, "hum": 60},
    "Sugarcane": {"N": 200, "P": 80, "K": 100,"pH": 6.8, "rain": 1600, "temp": 32, "hum": 80},
    "Soybean":   {"N": 30,  "P": 55, "K": 40, "pH": 6.5, "rain": 700,  "temp": 25, "hum": 70},
    "Groundnut": {"N": 22,  "P": 50, "K": 40, "pH": 6.2, "rain": 550,  "temp": 30, "hum": 60},
    "Tomato":    {"N": 125, "P": 75, "K": 100,"pH": 6.5, "rain": 500,  "temp": 25, "hum": 70},
    "Onion":     {"N": 100, "P": 60, "K": 70, "pH": 6.5, "rain": 450,  "temp": 22, "hum": 65},
    "Potato":    {"N": 150, "P": 80, "K": 125,"pH": 5.8, "rain": 500,  "temp": 20, "hum": 78},
}


def _encode_safe(encoder, value: str, fallback: int = 0) -> int:
    """Safely encode a categorical value, returning fallback if unknown."""
    try:
        return encoder.transform([value])[0]
    except (ValueError, KeyError):
        return fallback


def _get_confidence(model, X_scaled: np.ndarray) -> float:
    """
    Derive confidence score (0–100) from the variance across
    individual tree predictions in the random forest.
    Lower variance = higher confidence.
    """
    tree_preds = np.array([tree.predict(X_scaled) for tree in model.estimators_])
    std = tree_preds.std(axis=0)[0]
    mean_pred = abs(tree_preds.mean())
    if mean_pred == 0:
        return 50.0
    # Coefficient of variation → confidence
    cv = std / max(mean_pred, 1.0)
    confidence = max(0, min(100, 100 * (1 - cv * 2)))
    return round(confidence, 1)


def _generate_recommendations(crop: str, yield_per_acre: float, avg_yield: float,
                                N: float, P: float, K: float, pH: float,
                                rainfall: float, temperature: float) -> list:
    """Generate actionable farming recommendations when yield is suboptimal."""
    recs = []
    ideal = IDEAL_CONDITIONS.get(crop, {})
    if not ideal:
        return recs

    # NPK recommendations
    if N < ideal.get("N", 100) * 0.7:
        recs.append({
            "type": "fertilizer",
            "title": "Increase Nitrogen (N)",
            "detail": f"Current N ({N:.0f} kg/ha) is low. Apply {ideal['N'] - N:.0f} kg/ha more urea or ammonium sulfate for better vegetative growth.",
            "impact": "high"
        })
    if P < ideal.get("P", 50) * 0.7:
        recs.append({
            "type": "fertilizer",
            "title": "Increase Phosphorus (P)",
            "detail": f"Current P ({P:.0f} kg/ha) is below optimal. Add DAP or SSP fertilizer to improve root development.",
            "impact": "medium"
        })
    if K < ideal.get("K", 40) * 0.7:
        recs.append({
            "type": "fertilizer",
            "title": "Increase Potassium (K)",
            "detail": f"Current K ({K:.0f} kg/ha) is low. Apply muriate of potash (MOP) for better disease resistance.",
            "impact": "medium"
        })

    # pH recommendations
    if pH < 5.5:
        recs.append({
            "type": "soil",
            "title": "Soil Too Acidic",
            "detail": f"pH {pH:.1f} is acidic. Apply agricultural lime (2-4 tonnes/ha) to raise pH to optimal range.",
            "impact": "high"
        })
    elif pH > 7.5:
        recs.append({
            "type": "soil",
            "title": "Soil Too Alkaline",
            "detail": f"pH {pH:.1f} is alkaline. Apply gypsum or sulfur amendments to lower pH.",
            "impact": "high"
        })

    # Rainfall / irrigation
    ideal_rain = ideal.get("rain", 600)
    if rainfall < ideal_rain * 0.6:
        recs.append({
            "type": "irrigation",
            "title": "Low Rainfall — Increase Irrigation",
            "detail": f"Rainfall ({rainfall:.0f} mm) is significantly below the ideal ({ideal_rain} mm). Set up drip or sprinkler irrigation.",
            "impact": "high"
        })

    # Temperature stress
    ideal_temp = ideal.get("temp", 25)
    if temperature > ideal_temp + 8:
        recs.append({
            "type": "management",
            "title": "Heat Stress Warning",
            "detail": f"Temperature ({temperature:.1f}°C) is very high. Use mulching and ensure adequate watering during peak heat.",
            "impact": "high"
        })

    # Yield comparison
    if yield_per_acre < avg_yield * 0.8:
        # Suggest alternative crops with potentially higher yield
        alternatives = [c for c in IDEAL_CONDITIONS if c != crop]
        recs.append({
            "type": "crop_switch",
            "title": "Consider Alternative Crops",
            "detail": f"Your predicted yield is {((avg_yield - yield_per_acre)/avg_yield*100):.0f}% below the regional average. Consider crops like {', '.join(alternatives[:3])} which may perform better in your conditions.",
            "impact": "medium"
        })

    return recs


def predict_yield(
    crop_type: str,
    soil_type: str,
    rainfall_mm: float,
    temperature_c: float,
    land_size_acres: float,
    humidity: float = 65.0,
    soil_n: float = 80.0,
    soil_p: float = 40.0,
    soil_k: float = 40.0,
    soil_ph: float = 6.5,
):
    """
    Production ML-based yield prediction.
    Returns a rich dictionary with prediction, confidence, charts, and recommendations.
    """
    if not _model_loaded:
        # Graceful fallback if model hasn't been trained yet
        return {
            "expected_yield_per_acre": 0,
            "total_expected_yield": 0,
            "unit": "quintals",
            "confidence_score": 0,
            "avg_regional_yield": 0,
            "optimal_yield": 0,
            "recommendations": [{"type": "error", "title": "Model Not Trained", "detail": "Please run train_models.py first.", "impact": "high"}],
        }

    crop_name = crop_type.strip().capitalize()

    # ── 1. Prepare features ──
    crop_encoded = _encode_safe(_crop_encoder, crop_name)
    soil_encoded = _encode_safe(_soil_encoder, soil_type.strip().capitalize() if soil_type else "Loamy")

    features = np.array([[crop_encoded, soil_encoded, soil_n, soil_p, soil_k,
                           soil_ph, rainfall_mm, temperature_c, humidity]])
    features_scaled = _scaler.transform(features)

    # ── 2. Predict yield ──
    yield_per_acre = float(_model.predict(features_scaled)[0])
    yield_per_acre = max(yield_per_acre, 0.1)  # Never negative
    total_yield = yield_per_acre * land_size_acres

    # ── 3. Confidence score ──
    confidence = _get_confidence(_model, features_scaled)

    # ── 4. Regional average from training data ──
    crop_stats = _crop_averages.get(crop_name, {})
    avg_regional = crop_stats.get("mean", yield_per_acre * 0.9)
    best_case    = crop_stats.get("max", yield_per_acre * 1.3)

    # ── 5. Compute optimal scenario (ideal inputs) ──
    ideal = IDEAL_CONDITIONS.get(crop_name, {})
    if ideal:
        opt_features = np.array([[crop_encoded, soil_encoded,
                                   ideal.get("N", soil_n), ideal.get("P", soil_p),
                                   ideal.get("K", soil_k), ideal.get("pH", soil_ph),
                                   ideal.get("rain", rainfall_mm), ideal.get("temp", temperature_c),
                                   ideal.get("hum", humidity)]])
        opt_scaled = _scaler.transform(opt_features)
        optimal_yield = float(_model.predict(opt_scaled)[0])
    else:
        optimal_yield = yield_per_acre * 1.2

    # ── 6. AI Recommendations ──
    recommendations = _generate_recommendations(
        crop_name, yield_per_acre, avg_regional,
        soil_n, soil_p, soil_k, soil_ph, rainfall_mm, temperature_c
    )

    return {
        "expected_yield_per_acre": round(yield_per_acre, 2),
        "total_expected_yield": round(total_yield, 2),
        "unit": "quintals",
        "confidence_score": confidence,
        "avg_regional_yield": round(avg_regional, 2),
        "optimal_yield": round(optimal_yield, 2),
        "recommendations": recommendations,
    }
