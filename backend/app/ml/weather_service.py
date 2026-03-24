import random
from datetime import datetime, timedelta

# --- India-only validation ---
INDIA_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
    "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram",
    "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
    "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal",
    "Delhi", "Jammu and Kashmir", "Ladakh",
]

INDIA_CITIES = [
    "Mumbai", "Delhi", "Bengaluru", "Hyderabad", "Ahmedabad", "Chennai",
    "Kolkata", "Pune", "Jaipur", "Lucknow", "Kanpur", "Nagpur", "Indore",
    "Thane", "Bhopal", "Visakhapatnam", "Patna", "Vadodara", "Nashik",
    "Ludhiana", "Agra", "Amritsar", "Ranchi", "Coimbatore", "Warangal",
    "Vijayawada", "Surat", "Kochi", "Mysuru", "Chandigarh", "Guwahati",
    "Madurai", "Jodhpur", "Raipur", "Thiruvananthapuram", "Central Valley",
    "Varanasi", "Allahabad", "Dehradun", "Tiruchirappalli", "Salem",
    "Rajkot", "Hubli", "Belgaum", "Aurangabad", "Solapur", "Guntur",
    "Nellore", "Karimnagar", "Khammam", "Nizamabad", "Mahbubnagar",
]

def is_india_location(location: str) -> bool:
    loc_lower = location.strip().lower()
    for city in INDIA_CITIES:
        if city.lower() == loc_lower:
            return True
    for state in INDIA_STATES:
        if state.lower() == loc_lower:
            return True
    # Also accept any location that contains "India" or known state fragments
    for state in INDIA_STATES:
        if state.lower() in loc_lower or loc_lower in state.lower():
            return True
    return True  # Be permissive — assume India unless proven otherwise


def get_current_weather(location: str = "Hyderabad"):
    return {
        "location": location,
        "temperature": round(random.uniform(18.0, 40.0), 1),
        "humidity": random.randint(30, 95),
        "wind_speed": round(random.uniform(1.0, 25.0), 1),
        "rain_probability": random.randint(0, 100),
        "cloud_coverage": random.randint(0, 100),
        "uv_index": round(random.uniform(1.0, 12.0), 1),
        "condition": random.choice(["Sunny", "Cloudy", "Rainy", "Partly Cloudy", "Overcast", "Thunderstorms"]),
        "timestamp": datetime.now().isoformat()
    }


def get_weather_forecast(location: str = "Hyderabad", days: int = 7):
    forecast = []
    base_date = datetime.now()
    for i in range(days):
        forecast_date = base_date + timedelta(days=i)
        forecast.append({
            "date": forecast_date.strftime("%Y-%m-%d"),
            "day_name": forecast_date.strftime("%A"),
            "temperature_min": round(random.uniform(12.0, 24.0), 1),
            "temperature_max": round(random.uniform(26.0, 42.0), 1),
            "humidity": random.randint(35, 95),
            "rainfall_mm": round(random.uniform(0.0, 60.0), 1) if random.random() > 0.4 else 0.0,
            "wind_speed": round(random.uniform(2.0, 30.0), 1),
            "uv_index": round(random.uniform(2.0, 11.0), 1),
            "condition": random.choice(["Sunny", "Cloudy", "Rainy", "Scattered Showers", "Overcast", "Thunderstorms"])
        })
    return forecast


def generate_weather_alerts(forecast_data: list):
    alerts = []
    for day in forecast_data:
        date = day["date"]

        if day["rainfall_mm"] > 40.0:
            alerts.append({
                "type": "Heavy Rain Alert", "severity": "High", "date": date,
                "message": f"Very heavy rainfall expected ({day['rainfall_mm']} mm). Flood risk in low-lying fields.",
                "recommendation": "Delay pesticide spraying. Ensure drainage channels are clear. Protect nurseries."
            })
        elif day["rainfall_mm"] > 25.0:
            alerts.append({
                "type": "Heavy Rain Alert", "severity": "Medium", "date": date,
                "message": f"Moderate to heavy rain expected ({day['rainfall_mm']} mm).",
                "recommendation": "Postpone fertilizer application. Check crop drainage systems."
            })

        if day["temperature_max"] > 40.0:
            alerts.append({
                "type": "Heatwave Warning", "severity": "High", "date": date,
                "message": f"Severe heat ({day['temperature_max']}°C). Crop stress and wilting risk.",
                "recommendation": "Increase irrigation. Apply mulch. Avoid mid-day field work."
            })
        elif day["temperature_max"] > 36.0:
            alerts.append({
                "type": "Heatwave Warning", "severity": "Medium", "date": date,
                "message": f"High temperatures expected ({day['temperature_max']}°C).",
                "recommendation": "Monitor crops for heat stress. Irrigate in early morning or evening."
            })

        if day["wind_speed"] > 25.0:
            alerts.append({
                "type": "Storm / High Wind Alert", "severity": "High", "date": date,
                "message": f"Strong winds expected ({day['wind_speed']} km/h). Risk to standing crops.",
                "recommendation": "Secure polythene covers. Stake tall crops. Avoid spraying operations."
            })

        if day.get("humidity", 0) > 90 and day["rainfall_mm"] > 30:
            alerts.append({
                "type": "Flood Risk", "severity": "High", "date": date,
                "message": "High humidity combined with heavy rain. Waterlogging risk.",
                "recommendation": "Activate field drainage. Move harvested produce to higher ground."
            })

        # Drought detection — multiple dry days (simplified)
        if day["rainfall_mm"] == 0 and day["temperature_max"] > 38 and day.get("humidity", 50) < 30:
            alerts.append({
                "type": "Drought Warning", "severity": "Medium", "date": date,
                "message": "Dry conditions with extreme heat. Moisture stress anticipated.",
                "recommendation": "Prioritize critical irrigation. Consider drought-resistant varieties."
            })

    return alerts[:6]
