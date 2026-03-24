# app/ml/fertilizer_recommendation.py

def get_fertilizer_recommendation(crop_type: str, soil_type: str, season: str):
    """
    Generates tailored NPK fertilizer recommendations.
    """
    base_npk = {
        "Rice": {"N": 80, "P": 40, "K": 40},
        "Wheat": {"N": 120, "P": 60, "K": 40},
        "Maize": {"N": 100, "P": 50, "K": 50},
        "Cotton": {"N": 120, "P": 60, "K": 60},
        "Sugarcane": {"N": 150, "P": 80, "K": 80},
    }
    
    crop = crop_type.capitalize()
    npk = base_npk.get(crop, {"N": 50, "P": 30, "K": 30})
    
    # Adjust based on soil
    if soil_type.lower() == "black":
        npk["K"] = max(0, npk["K"] - 10) # Black soil usually rich in potash
    elif soil_type.lower() == "sandy":
        npk["N"] += 20 # Leaches easily
        
    advice_map = {
        "Rice": "Apply urea in 3 splits: basal, maximum tillering, and panicle initiation.",
        "Wheat": "Apply half dose of nitrogen and full dose of P & K at sowing. Remaining N at first irrigation.",
        "Maize": "Apply basal NPK at sowing, top dress remaining N at knee-high stage.",
        "Cotton": "Apply balanced NPK at square formation.",
        "Sugarcane": "Heavy basal application required. Top dress N after 60 and 90 days."
    }
    
    return {
        "nitrogen_kg_per_acre": npk["N"],
        "phosphorus_kg_per_acre": npk["P"],
        "potassium_kg_per_acre": npk["K"],
        "advice": advice_map.get(crop, "Apply basal dose at sowing and top dress nitrogen later.")
    }
