from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.models.scheme_model import Scheme, FarmerInput, RecommendationResult
from app.schemas.scheme_schema import SchemeRecommendationRequest
from app.ml.scheme_recommender import SchemeRecommender

class SchemeService:
    def __init__(self, db: Session):
        self.db = db
        self.recommender = SchemeRecommender()
        self._seed_schemes_if_empty()

    def _seed_schemes_if_empty(self):
        """Seed initial schemes to the DB from the JSON dataset if it is empty."""
        existing = self.db.query(Scheme).first()
        if not existing:
            for scheme_data in self.recommender.schemes:
                scheme = Scheme(
                    name=scheme_data.get("scheme_name"),
                    description=scheme_data.get("description"),
                    states=scheme_data.get("states"),
                    soil_types=scheme_data.get("soil_types"),
                    water_requirement=scheme_data.get("water_requirement"),
                    recommended_crops=scheme_data.get("recommended_crops"),
                    benefits=scheme_data.get("benefits"),
                    official_link=scheme_data.get("official_link")
                )
                self.db.add(scheme)
            self.db.commit()

    def get_scheme_recommendations(self, request: SchemeRecommendationRequest) -> Dict[str, Any]:
        """Process farmer input and return eligible schemes."""
        
        # 1. Save input to DB
        farmer_input = FarmerInput(
            soil_type=request.soil_type,
            land_size=request.land_size,
            water_availability=request.water_availability,
            location_state=request.state,
            location_district=request.district
        )
        self.db.add(farmer_input)
        self.db.commit()
        self.db.refresh(farmer_input)

        # 2. Filter using ML/Rule Submodule directly from JSON dataset
        eligible_schemes = self.recommender.recommend_schemes(
            soil_type=request.soil_type,
            land_size=request.land_size,
            water_availability=request.water_availability,
            state=request.state,
            district=request.district
        )

        recommended_scheme_names = [s["name"] for s in eligible_schemes]

        # 3. Save result
        result = RecommendationResult(
            farmer_input_id=farmer_input.id,
            recommended_schemes=recommended_scheme_names, # we keep names for the DB storage
            recommended_crops=[],
            entrepreneur_opportunities=[]
        )
        self.db.add(result)
        self.db.commit()

        return {"recommended_schemes": eligible_schemes}
