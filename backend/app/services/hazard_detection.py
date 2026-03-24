"""
Hazard Monitoring System
Analyzes weather data to produce a composite hazard assessment for agricultural regions.
"""

def detect_hazards(weather: dict, forecast: list):
    hazards = []
    temp = weather.get("temperature", 30)
    humidity = weather.get("humidity", 50)
    wind = weather.get("wind_speed", 5)
    rain_prob = weather.get("rain_probability", 0)
    location = weather.get("location", "Unknown")

    # Aggregate forecast rainfall
    total_forecast_rain = sum(d.get("rainfall_mm", 0) for d in forecast)
    max_temp = max((d.get("temperature_max", 30) for d in forecast), default=30)
    max_wind = max((d.get("wind_speed", 5) for d in forecast), default=5)
    dry_days = sum(1 for d in forecast if d.get("rainfall_mm", 0) == 0)

    # --- Heatwave ---
    if max_temp > 40:
        hazards.append({
            "hazard": "Heatwave", "risk_level": "High",
            "region": location, "icon": "🔥",
            "description": f"Temperatures reaching {max_temp}°C. Crop heat stress likely.",
            "mitigation": "Increase irrigation. Apply mulch. Avoid field work 11 AM–3 PM. Consider shade nets for sensitive crops."
        })
    elif max_temp > 36:
        hazards.append({
            "hazard": "Heatwave", "risk_level": "Medium",
            "region": location, "icon": "🔥",
            "description": f"Elevated temperatures up to {max_temp}°C expected.",
            "mitigation": "Monitor crops for heat stress. Schedule irrigation during cooler hours."
        })

    # --- Flood Risk ---
    if total_forecast_rain > 150:
        hazards.append({
            "hazard": "Flood Risk", "risk_level": "High",
            "region": location, "icon": "🌊",
            "description": f"Cumulative rainfall of {total_forecast_rain:.0f} mm over the next 7 days.",
            "mitigation": "Clear drainage channels. Move produce to elevated storage. Prepare emergency crop coverage."
        })
    elif total_forecast_rain > 80:
        hazards.append({
            "hazard": "Flood Risk", "risk_level": "Medium",
            "region": location, "icon": "🌊",
            "description": f"Moderate cumulative rainfall ({total_forecast_rain:.0f} mm) expected.",
            "mitigation": "Ensure field drainage is functional. Delay sowing in low-lying areas."
        })

    # --- Cyclone Risk ---
    if max_wind > 30 and total_forecast_rain > 100:
        hazards.append({
            "hazard": "Cyclone Risk", "risk_level": "High",
            "region": location, "icon": "🌀",
            "description": f"Extreme winds ({max_wind} km/h) with heavy rainfall. Cyclonic conditions possible.",
            "mitigation": "Secure greenhouses and polythene. Harvest mature crops immediately. Follow NDMA advisories."
        })

    # --- Drought Risk ---
    if dry_days >= 5 and max_temp > 36:
        hazards.append({
            "hazard": "Drought Risk", "risk_level": "High" if dry_days >= 6 else "Medium",
            "region": location, "icon": "☀️",
            "description": f"{dry_days} consecutive dry days forecasted with high temperatures.",
            "mitigation": "Prioritize water-stressed fields. Use drip irrigation. Consider drought-tolerant crop varieties."
        })

    # --- Pest Outbreak Risk ---
    if humidity > 75 and temp > 25:
        hazards.append({
            "hazard": "Pest Outbreak Risk", "risk_level": "High" if humidity > 85 else "Medium",
            "region": location, "icon": "🐛",
            "description": f"High humidity ({humidity}%) with warm temps ({temp}°C) — ideal for pest proliferation.",
            "mitigation": "Increase field scouting. Deploy pheromone traps. Prepare preventive pesticide applications."
        })

    # --- Heavy Rainfall hazard ---
    heavy_rain_days = sum(1 for d in forecast if d.get("rainfall_mm", 0) > 30)
    if heavy_rain_days >= 2:
        hazards.append({
            "hazard": "Heavy Rainfall", "risk_level": "High",
            "region": location, "icon": "🌧️",
            "description": f"{heavy_rain_days} days of heavy rain (>30mm) expected.",
            "mitigation": "Delay fertilizer and pesticide application. Protect nursery beds. Ensure drainage."
        })

    return hazards[:8]
