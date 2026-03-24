from typing import List, Dict, Any

class CropRecommender:
    def __init__(self):
        # We can hardcode ideal conditions for major crops
        self.crop_conditions = {
            "Rice": {"n": (80, 150), "p": (40, 60), "k": (40, 60), "ph": (5.5, 7.0), "water": ["Good"], "soil": ["Alluvial", "Clay", "Black"]},
            "Wheat": {"n": (100, 120), "p": (50, 60), "k": (40, 60), "ph": (6.0, 7.5), "water": ["Medium", "Good"], "soil": ["Alluvial", "Black"]},
            "Cotton": {"n": (100, 150), "p": (40, 60), "k": (40, 80), "ph": (5.8, 8.0), "water": ["Medium", "Good"], "soil": ["Black", "Alluvial", "Red"]},
            "Turmeric": {"n": (100, 120), "p": (40, 60), "k": (60, 100), "ph": (5.5, 7.5), "water": ["Medium", "Good"], "soil": ["Red", "Alluvial", "Black"]},
            "Maize": {"n": (80, 120), "p": (40, 60), "k": (40, 60), "ph": (5.8, 7.5), "water": ["Medium", "Good"], "soil": ["Alluvial", "Red", "Black"]},
            "Sugarcane": {"n": (150, 250), "p": (60, 100), "k": (60, 100), "ph": (6.0, 8.0), "water": ["Good"], "soil": ["Black", "Alluvial", "Red"]},
            "Millets": {"n": (20, 60), "p": (15, 30), "k": (15, 30), "ph": (5.5, 8.0), "water": ["Poor", "Medium"], "soil": ["Red", "Sandy", "Laterite", "Black"]},
            "Pulses": {"n": (20, 40), "p": (40, 50), "k": (20, 30), "ph": (6.0, 7.5), "water": ["Poor", "Medium", "Good"], "soil": ["Red", "Black", "Alluvial"]},
            "Vegetables": {"n": (80, 100), "p": (40, 60), "k": (40, 60), "ph": (5.5, 7.0), "water": ["Good", "Medium"], "soil": ["Alluvial", "Red"]},
            "Tomato": {"n": (80, 100), "p": (40, 60), "k": (60, 80), "ph": (6.0, 7.0), "water": ["Good", "Medium"], "soil": ["Red", "Alluvial", "Black"]},
            "Chili": {"n": (80, 120), "p": (40, 60), "k": (40, 60), "ph": (6.0, 7.0), "water": ["Medium", "Good"], "soil": ["Black", "Red"]}
        }
        
        self.entrepreneur_ideas = {
            "Turmeric": {"business_opportunity": "Turmeric powder processing unit", "processing_idea": "Grinding, packaging, and sorting into high-curcumin pure turmeric powder.", "expected_profit_potential": "₹2L - ₹5L per annum (High Margin)"},
            "Tomato": {"business_opportunity": "Tomato powder production", "processing_idea": "Dehydrating tomatoes into powder and making preservative-free puree.", "expected_profit_potential": "₹3L - ₹6L per annum (Value Addition)"},
            "Chili": {"business_opportunity": "Chili powder packaging", "processing_idea": "Sun-drying, stem-cutting, grinding and standard packaging.", "expected_profit_potential": "₹1.5L - ₹4L per annum"},
            "Maize": {"business_opportunity": "Maize feed processing", "processing_idea": "Crushing maize with other additives to create high-nutrition poultry/cattle feed.", "expected_profit_potential": "₹4L - ₹8L per annum (Bulk Scale)"},
            "Millets": {"business_opportunity": "Millet flour products", "processing_idea": "Milling into multi-grain flours and baking healthy cookies/rusks.", "expected_profit_potential": "₹2L - ₹5L per annum (Health Trend)"},
            "Cotton": {"business_opportunity": "Surgical Cotton & Oilseed Extraction", "processing_idea": "Extracting cotton seed oil and purifying cotton for medical use.", "expected_profit_potential": "₹5L - ₹10L per annum (Capital Intensive)"},
            "Sugarcane": {"business_opportunity": "Jaggery & Ethanol Production", "processing_idea": "Boiling cane juice for organic jaggery or fermenting for ethanol.", "expected_profit_potential": "₹10L+ per annum"},
            "Rice": {"business_opportunity": "Rice Bran Oil Processing", "processing_idea": "Extracting healthy cooking oil from rice bran.", "expected_profit_potential": "₹8L+ per annum"},
            "Wheat": {"business_opportunity": "Bakery & Biscuits Unit", "processing_idea": "Processing wheat down to Maida/Atta and baking products.", "expected_profit_potential": "₹3L - ₹6L per annum"},
            "Pulses": {"business_opportunity": "Dal Mill", "processing_idea": "Cleaning, grading, and splitting raw pulses.", "expected_profit_potential": "₹4L - ₹7L per annum"},
            "Vegetables": {"business_opportunity": "Cold Storage & Supply Chain", "processing_idea": "Setting up a micro cold-storage facility to reduce wastage and sell off-season.", "expected_profit_potential": "₹5L - ₹12L per annum"}
        }

    def recommend_crops(self, soil_type: str, n: float, p: float, k: float, ph: float, water: str, state: str) -> List[Dict[str, Any]]:
        recommendations = []
        soil_type_title = soil_type.title()
        water_title = water.title()
        
        for crop, cond in self.crop_conditions.items():
            score = 100.0
            
            # Soil check
            if soil_type_title not in cond["soil"] and "All" not in cond["soil"]:
                score -= 30.0
                
            # Water check
            if water_title not in cond["water"]:
                score -= 25.0
                
            # pH check
            if not (cond["ph"][0] <= ph <= cond["ph"][1]):
                score -= 15.0
                
            # NPK checks
            if not (cond["n"][0] <= n <= cond["n"][1]):
                score -= 10.0
            if not (cond["p"][0] <= p <= cond["p"][1]):
                score -= 10.0
            if not (cond["k"][0] <= k <= cond["k"][1]):
                score -= 10.0
                
            if score >= 50:
                recommendations.append({
                    "crop_name": crop.lower(), # matching example output case
                    "suitability_score": max(50.0, score)
                })
                
        # Sort by score descending
        recommendations.sort(key=lambda x: x["suitability_score"], reverse=True)
        return recommendations[:5] # Return top 5

    def get_entrepreneur_opportunities(self, crops: List[str]) -> List[Dict[str, str]]:
        opportunities = []
        for crop in crops:
            crop_title = crop.title()
            if crop_title in self.entrepreneur_ideas:
                idea = self.entrepreneur_ideas[crop_title]
                opportunities.append({
                    "crop": crop_title,
                    "business_opportunity": idea["business_opportunity"],
                    "processing_idea": idea["processing_idea"],
                    "expected_profit_potential": idea["expected_profit_potential"]
                })
        
        if not opportunities:
            opportunities.append({
                "crop": "General Agriculture",
                "business_opportunity": "Agro-Processing Unit",
                "processing_idea": "Value-addition, grading, and packaging of local farm produce.",
                "expected_profit_potential": "₹2L - ₹4L per annum"
            })
            
        return opportunities
