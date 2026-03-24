"""
Crop Disease Risk Detection Module
Analyzes weather conditions to estimate crop disease risk using rule-based heuristics.
"""

def predict_disease_risk(crop: str, temperature: float, humidity: int, rainfall_mm: float, cloud_coverage: int = 50):
    crop_lower = crop.lower().strip() if crop else "general"

    risk_level = "Low"
    disease = "No significant disease threat detected"
    recommendation = "Continue regular crop monitoring. Maintain field hygiene."

    # --- High humidity + cloudy = fungal diseases ---
    if humidity > 80 and cloud_coverage > 60:
        risk_level = "High"
        if crop_lower in ["tomato", "potato"]:
            disease = "Late Blight (Phytophthora infestans)"
            recommendation = "Apply copper-based fungicide immediately. Improve field drainage and air circulation. Remove infected plant parts."
        elif crop_lower in ["rice", "paddy"]:
            disease = "Blast Disease (Magnaporthe oryzae)"
            recommendation = "Apply Tricyclazole-based fungicide. Avoid excess nitrogen fertilizer. Maintain proper water management."
        elif crop_lower in ["wheat"]:
            disease = "Yellow Rust (Puccinia striiformis)"
            recommendation = "Apply Propiconazole spray. Scout fields every 3 days. Use resistant varieties next season."
        elif crop_lower in ["cotton"]:
            disease = "Grey Mildew (Ramularia areola)"
            recommendation = "Apply Carbendazim spray. Remove lower infected leaves. Improve spacing for air flow."
        elif crop_lower in ["chili", "chilli"]:
            disease = "Anthracnose (Colletotrichum capsici)"
            recommendation = "Apply Mancozeb spray. Harvest ripe fruits early. Avoid overhead irrigation."
        elif crop_lower in ["maize", "corn"]:
            disease = "Turcicum Leaf Blight"
            recommendation = "Apply Zineb or Mancozeb. Use resistant hybrids. Remove crop debris after harvest."
        else:
            disease = "Fungal Leaf Spot / Powdery Mildew"
            recommendation = "Apply broad-spectrum fungicide. Ensure proper crop spacing and drainage."

    # --- Warm + humid = bacterial diseases ---
    elif humidity > 70 and temperature > 28:
        risk_level = "Medium"
        if crop_lower in ["rice", "paddy"]:
            disease = "Bacterial Leaf Blight (Xanthomonas oryzae)"
            recommendation = "Avoid excess nitrogen. Drain standing water. Apply Streptocycline if infection confirmed."
        elif crop_lower in ["tomato"]:
            disease = "Bacterial Wilt (Ralstonia solanacearum)"
            recommendation = "Remove wilted plants. Avoid waterlogging. Rotate crops with non-solanaceous species."
        else:
            disease = "Bacterial Soft Rot risk"
            recommendation = "Maintain field sanitation. Avoid injury to fruits during handling."

    # --- Humid + warm + rainy = viral spread via vectors ---
    elif humidity > 65 and temperature > 25 and rainfall_mm > 10:
        risk_level = "Medium"
        if crop_lower in ["cotton"]:
            disease = "Cotton Leaf Curl Virus (CLCuV)"
            recommendation = "Control whitefly population with neem oil or imidacloprid. Use virus-resistant Bt cotton varieties."
        elif crop_lower in ["chili", "chilli"]:
            disease = "Chili Leaf Curl Virus"
            recommendation = "Manage whitefly vectors with sticky traps and neem-based sprays."
        else:
            disease = "Vector-borne viral disease risk"
            recommendation = "Control sucking pests (aphids, whiteflies, thrips) which act as virus vectors."

    return {
        "crop": crop,
        "disease": disease,
        "risk_level": risk_level,
        "recommendation": recommendation,
        "factors": {
            "temperature": temperature,
            "humidity": humidity,
            "rainfall_mm": rainfall_mm,
            "cloud_coverage": cloud_coverage
        }
    }
