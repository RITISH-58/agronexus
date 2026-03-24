import json
import os
from typing import List, Dict, Any

class SchemeRecommender:
    def __init__(self):
        self.dataset_path = os.path.join(os.path.dirname(__file__), "../data/schemes.json")
        self.schemes = self._load_schemes()

    def _load_schemes(self) -> List[Dict[str, Any]]:
        if os.path.exists(self.dataset_path):
            with open(self.dataset_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def recommend_schemes(self, soil_type: str, land_size: float, water_availability: str, state: str, district: str) -> List[Dict[str, Any]]:
        eligible = []
        state_title = state.title()
        soil_type_title = soil_type.title()
        water_availability_title = water_availability.title()

        for scheme in self.schemes:
            # Check State
            states = scheme.get("states", [])
            if "All" not in states and state_title not in states:
                continue
                
            # Check Soil
            soils = scheme.get("soil_types", [])
            if "All" not in soils and soil_type_title not in soils:
                continue
                
            # Check Water
            water_reqs = scheme.get("water_requirement", [])
            if "All" not in water_reqs and water_availability_title not in water_reqs:
                continue
            
            eligible.append({
                "name": scheme["scheme_name"],
                "benefit": scheme["benefits"],
                "link": scheme["official_link"]
            })
            
        return eligible
