def predict_pest_risk(crop: str, temperature: float, humidity: int, rainfall_mm: float):
    crop_lower = crop.lower() if crop else "unknown"
    
    risk_level = "Low"
    identified_pest = "Generic Pests"
    recommendation = "Maintain standard scouting monitoring protocols."
    
    # Generic Rule-based Engine
    if temperature > 25 and humidity > 75:
        risk_level = "High"
        
        if crop_lower in ["rice", "paddy"]:
            identified_pest = "Brown Planthopper"
            recommendation = "Apply preventive pesticide spray immediately. Ensure proper drainage to reduce humidity."
        elif crop_lower in ["cotton"]:
            identified_pest = "Bollworm"
            recommendation = "Scout for eggs and early instar larvae. Consider releasing biological control agents."
        elif crop_lower in ["wheat"]:
            identified_pest = "Aphids"
            recommendation = "Monitor field edges. If threshold exceeded, apply systemic insecticide."
        else:
            identified_pest = "Fungal Pathogens / Mildew"
            recommendation = "Favorable conditions for fungal growth. Apply preventive fungicide."
            
    elif temperature > 20 and humidity > 60:
        risk_level = "Medium"
        recommendation = "Increase field scouting frequency. Prepare intervention strategies if conditions worsen."
        if crop_lower == "corn" or crop_lower == "maize":
            identified_pest = "Fall Armyworm"
            
    # Rainfall washing away pests or increasing fungal rot
    if rainfall_mm > 20:
        if risk_level == "High":
            recommendation += " Note: Heavy rain may wash away topical applications. Delay spraying."
            
    return {
        "crop": crop,
        "risk_level": risk_level,
        "identified_pest": identified_pest,
        "recommendation": recommendation,
        "factors": {
            "temperature": temperature,
            "humidity": humidity,
            "rainfall_mm": rainfall_mm
        }
    }
