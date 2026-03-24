"""
Smart Irrigation Advisor Module
Generates irrigation recommendations based on weather forecast, temperature, humidity, and crop water needs.
"""

CROP_WATER_NEEDS = {
    "rice": "High", "paddy": "High", "sugarcane": "High",
    "wheat": "Medium", "maize": "Medium", "corn": "Medium", "cotton": "Medium",
    "millets": "Low", "pulses": "Low", "groundnut": "Low",
    "tomato": "Medium", "chili": "Medium", "chilli": "Medium",
    "potato": "Medium", "turmeric": "Medium",
}


def get_irrigation_advice(crop: str, temperature: float, humidity: int, rain_forecast_mm: float, recent_rainfall_mm: float = 0.0):
    crop_lower = crop.lower().strip() if crop else "general"
    water_need = CROP_WATER_NEEDS.get(crop_lower, "Medium")

    advice_lines = []
    urgency = "Normal"
    action = "Follow regular irrigation schedule."

    # --- Rain expected → delay irrigation ---
    if rain_forecast_mm > 20:
        urgency = "Low"
        action = "Delay irrigation. Significant rain expected."
        advice_lines.append(f"Rainfall of {rain_forecast_mm} mm forecasted. Skip today's irrigation to conserve water and prevent waterlogging.")
        if water_need == "High":
            advice_lines.append("For water-intensive crops, resume irrigation only if rain doesn't materialize within 24 hrs.")

    elif rain_forecast_mm > 5:
        urgency = "Low"
        action = "Reduce irrigation volume. Light rain expected."
        advice_lines.append(f"Light rain ({rain_forecast_mm} mm) expected. Reduce irrigation by 50%.")

    # --- Hot and dry → increase irrigation ---
    elif temperature > 38 and humidity < 40 and rain_forecast_mm < 2:
        urgency = "High"
        action = "Increase irrigation frequency immediately."
        advice_lines.append("Extreme heat with dry conditions detected. Crops at high risk of wilting.")
        advice_lines.append("Irrigate in early morning (before 7 AM) or late evening (after 6 PM) to minimize evaporation.")
        if water_need == "High":
            advice_lines.append("Water-intensive crop detected — apply 20% more water than usual schedule.")

    elif temperature > 34 and humidity < 50:
        urgency = "Medium"
        action = "Schedule extra irrigation."
        advice_lines.append("Elevated temperatures with moderate dryness. Consider an additional irrigation cycle.")
        advice_lines.append("Mulching around crop base can reduce soil moisture loss by up to 30%.")

    # --- Recent heavy rain → skip ---
    elif recent_rainfall_mm > 30:
        urgency = "Low"
        action = "No irrigation needed."
        advice_lines.append(f"Recent rainfall ({recent_rainfall_mm} mm) has saturated the soil. Irrigating now may cause waterlogging.")
        advice_lines.append("Allow 24-48 hours for excess water to drain before next irrigation.")

    # --- Normal conditions ---
    else:
        urgency = "Normal"
        action = "Follow regular irrigation schedule."
        if water_need == "High":
            advice_lines.append("Maintain consistent moisture for water-intensive crops. Monitor soil moisture daily.")
        elif water_need == "Low":
            advice_lines.append("Crop has low water needs. Irrigate only when top 2 inches of soil are dry.")
        else:
            advice_lines.append("Standard conditions. Continue regular irrigation as per schedule.")

    return {
        "crop": crop,
        "water_need_level": water_need,
        "urgency": urgency,
        "action": action,
        "detailed_advice": advice_lines,
        "factors": {
            "temperature": temperature,
            "humidity": humidity,
            "rain_forecast_mm": rain_forecast_mm,
            "recent_rainfall_mm": recent_rainfall_mm
        }
    }
