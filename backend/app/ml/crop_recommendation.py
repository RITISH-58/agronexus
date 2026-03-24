# app/ml/crop_recommendation.py

def get_companion_crops(main_crop: str):
    """
    Suggests companion crops for risk reduction and diversified income.
    """
    comps = {
        "Rice": ["Fish (Paddy-Fish farming)", "Azolla", "Dhaincha (Green Manure)"],
        "Wheat": ["Mustard", "Chickpea", "Linseed"],
        "Maize": ["Cowpea", "Soybean", "Green Gram"],
        "Cotton": ["Green Gram", "Black Gram", "Groundnut"],
        "Sugarcane": ["Onion", "Garlic", "Potato", "Moong"],
        "Tomato": ["Marigold (nematode control)", "Basil", "Onion"]
    }
    
    crop = main_crop.capitalize()
    return {
        "main_crop": crop,
        "recommended_companion_crops": comps.get(crop, ["Legumes", "Leafy Vegetables"]),
        "benefits": [
            "Diversified income source",
            "Improved soil health and nitrogen fixation",
            "Reduced total financial risk from monoculture price crashes",
            "Natural pest deterrence"
        ]
    }

def get_seasonal_alternatives(season: str, location: str):
    """
    Recommends alternative crops for the given season.
    """
    s = season.lower()
    if s == "kharif":
        crops = ["Rice", "Cotton", "Maize", "Turmeric", "Soybean", "Groundnut"]
    elif s == "rabi":
        crops = ["Wheat", "Mustard", "Chickpea", "Barley", "Oats"]
    elif s == "summer":
        crops = ["Watermelon", "Cucumber", "Green Gram", "Fodder Crops"]
    else:
        crops = ["Vegetables", "Legumes"]
        
    return {
        "season": season.capitalize(),
        "alternatives": crops
    }
