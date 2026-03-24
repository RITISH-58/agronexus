def get_farming_advice(crop: str, soil_type: str, weather_conditions: dict):
    # This acts as a mocked AI logic system based on current parameter heuristics
    advice = []
    
    temp = weather_conditions.get("temperature", 25.0)
    rain_prob = weather_conditions.get("rain_probability", 0)
    humidity = weather_conditions.get("humidity", 50)
    rain_mm = weather_conditions.get("rainfall_mm", 0.0)
    
    # Irrigation advice
    if rain_prob > 70 or rain_mm > 10:
        advice.append({
            "category": "Irrigation",
            "title": "Delay Irrigation",
            "description": f"High probability of rain ({rain_prob}%). Natural watering is sufficient."
        })
    elif temp > 32 and humidity < 40:
        advice.append({
            "category": "Irrigation",
            "title": "Increase Irrigation",
            "description": "High temperature and low humidity detected. Prevent crop thermal stress."
        })
        
    # Fertilizer advice
    if rain_prob > 80:
        advice.append({
            "category": "Fertilizer",
            "title": "Hold Fertilizer",
            "description": "Heavy rain expected. Avoid application today to prevent runoff and waste."
        })
    elif rain_prob > 30 and rain_prob <= 60:
        advice.append({
            "category": "Fertilizer",
            "title": "Optimal Fertilization Window",
            "description": "Light rain expected. Good conditions for fertilizer absorption."
        })

    # Pesticide Activity
    if rain_prob > 50:
         advice.append({
            "category": "Pesticide",
            "title": "Postpone Spraying",
            "description": "Rain likely to wash off topical applications. Wait for clear weather."
        })
    elif humidity > 80:
         advice.append({
            "category": "Pesticide",
            "title": "Fungicide Preparation",
            "description": "High humidity often accelerates fungal diseases. Monitor closely."
        })
        
    # Crop Specific Advice
    crop_lower = crop.lower() if crop else ""
    if crop_lower == "wheat" and temp > 30:
        advice.append({
            "category": "Crop Specific",
            "title": "Heat Stress Monitoring",
            "description": "Wheat is susceptible to yield loss at high temperatures during grain filling."
        })
    
    # Soil Specific Advice
    soil_lower = soil_type.lower() if soil_type else ""
    if "clay" in soil_lower and rain_mm > 20:
        advice.append({
            "category": "Soil Management",
            "title": "Drainage Check",
            "description": "Clay soils prone to waterlogging after heavy rain. Ensure proper field drainage."
        })
    elif "sandy" in soil_lower and temp > 30:
         advice.append({
            "category": "Soil Management",
            "title": "Moisture Retention",
            "description": "Sandy soils lose moisture rapidly. Consider mulching or frequent light irrigation."
        })
        
    # Fallback if conditions are perfect
    if len(advice) == 0:
        advice.append({
            "category": "General",
            "title": "Optimal Conditions",
            "description": "Current weather and soil conditions are optimal for general farming activities."
        })

    return {
        "summary": "AI Farming Advice generated based on current parameters.",
        "recommendations": advice
    }
