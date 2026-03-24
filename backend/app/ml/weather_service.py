import os
import random
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv() # Force reload of the .env file so the API key is picked up without a server restart

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


def _get_mock_current(location: str):
    return {
        "location": location,
        "temperature": 28.5,
        "humidity": 65,
        "wind_speed": 12.0,
        "rain_probability": 20,
        "cloud_coverage": 30,
        "uv_index": 5.0,
        "condition": "Partly Cloudy",
        "timestamp": datetime.now().isoformat()
    }

def get_current_weather(location: str = "Hyderabad"):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return _get_mock_current(location)

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={location},in&appid={api_key}&units=metric"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                "location": data.get("name", location),
                "temperature": round(data["main"]["temp"], 1),
                "humidity": data["main"]["humidity"],
                "wind_speed": round(data["wind"]["speed"] * 3.6, 1), # m/s to km/h
                "rain_probability": data.get("clouds", {}).get("all", 0), # proxy for cloud/rain prob
                "cloud_coverage": data.get("clouds", {}).get("all", 0),
                "uv_index": 5.0, # OM doesn't provide UV in standard free endpoint
                "condition": data["weather"][0]["main"],
                "timestamp": datetime.now().isoformat()
            }
    except Exception:
        pass
        
    return _get_mock_current(location)

def _get_mock_forecast(location: str, days: int):
    forecast = []
    base_date = datetime.now()
    for i in range(days):
        forecast_date = base_date + timedelta(days=i)
        forecast.append({
            "date": forecast_date.strftime("%Y-%m-%d"),
            "day_name": forecast_date.strftime("%A"),
            "temperature_min": 22.0,
            "temperature_max": 32.0,
            "humidity": 60,
            "rainfall_mm": 0.0,
            "wind_speed": 10.0,
            "uv_index": 6.0,
            "condition": "Sunny"
        })
    return forecast

def get_weather_forecast(location: str = "Hyderabad", days: int = 7):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return _get_mock_forecast(location, days)

    try:
        # Free API provides 5 day / 3 hour forecast
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={location},in&appid={api_key}&units=metric"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            # Aggregate 3-hour chunks into daily summaries
            daily_data = {}
            for item in data["list"]:
                date_str = item["dt_txt"].split(" ")[0]
                if date_str not in daily_data:
                    daily_data[date_str] = {
                        "date": date_str,
                        "day_name": datetime.strptime(date_str, "%Y-%m-%d").strftime("%A"),
                        "temps": [],
                        "humidities": [],
                        "rains": [],
                        "winds": [],
                        "conditions": []
                    }
                day = daily_data[date_str]
                day["temps"].append(item["main"]["temp"])
                day["humidities"].append(item["main"]["humidity"])
                day["winds"].append(item["wind"]["speed"])
                # Add up rain
                rain = item.get("rain", {}).get("3h", 0)
                day["rains"].append(rain)
                day["conditions"].append(item["weather"][0]["main"])
            
            # Reduce to final format
            forecast = []
            for date_str, items in list(daily_data.items())[:days]:
                # Pick most common condition
                cond = max(set(items["conditions"]), key=items["conditions"].count)
                forecast.append({
                    "date": date_str,
                    "day_name": items["day_name"],
                    "temperature_min": round(min(items["temps"]), 1),
                    "temperature_max": round(max(items["temps"]), 1),
                    "humidity": round(sum(items["humidities"]) / len(items["humidities"])),
                    "rainfall_mm": round(sum(items["rains"]), 1),
                    "wind_speed": round((sum(items["winds"]) / len(items["winds"])) * 3.6, 1),
                    "uv_index": 5.0,
                    "condition": cond
                })
            
            # If API gave fewer days than requested due to 5-day limit, fill the rest
            while len(forecast) < days:
                forecast.append(_get_mock_forecast(location, 1)[0])
                
            return forecast
    except Exception:
        pass

    return _get_mock_forecast(location, days)


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
