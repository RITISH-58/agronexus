import json
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.agri_business_model import AgriBusiness

class BusinessService:
    def search_businesses(self, db: Session, query: Optional[str] = None):
        """Search businesses by crop type, category, or business name."""
        base_query = db.query(AgriBusiness)
        
        if query and query.strip():
            search_term = f"%{query.strip().lower()}%"
            # Since SQLite doesn't natively support case-insensitive ilike as easily without config,
            # we'll just do normal like knowing data is mostly capitalized but users might type lower.
            base_query = base_query.filter(
                or_(
                    AgriBusiness.business_name.like(f"%{query.strip()}%"),
                    AgriBusiness.business_name.ilike(search_term),
                    AgriBusiness.crop_type.ilike(search_term),
                    AgriBusiness.category.ilike(search_term)
                )
            )
            
        results = base_query.all()
        
        # We only need the basic fields for the list response
        businesses = []
        for r in results:
            businesses.append({
                "id": r.id,
                "business_name": r.business_name,
                "crop_type": r.crop_type,
                "category": r.category,
                "investment": r.investment,
                "roi": r.roi,
                "revenue_range": r.revenue_range,
                "profit_margin": r.profit_margin,
                "break_even": r.break_even,
                "market_demand_level": r.market_demand_level
            })
            
        return {"businesses": businesses, "total": len(businesses)}

    def get_business_details(self, db: Session, business_id: int):
        """Get full blueprint details for a single business."""
        r = db.query(AgriBusiness).filter(AgriBusiness.id == business_id).first()
        if not r:
            return None
            
        # Parse all JSON strings back into objects
        try:
            return {
                "id": r.id,
                "business_name": r.business_name,
                "crop_type": r.crop_type,
                "category": r.category,
                "investment": r.investment,
                "roi": r.roi,
                "revenue_range": r.revenue_range,
                "profit_margin": r.profit_margin,
                "break_even": r.break_even,
                "market_demand_level": r.market_demand_level,
                "investment_breakdown": json.loads(r.investment_breakdown) if r.investment_breakdown else {},
                "production_capacity": json.loads(r.production_capacity) if r.production_capacity else {},
                "revenue_projection": json.loads(r.revenue_projection) if r.revenue_projection else {},
                "market_demand": json.loads(r.market_demand) if r.market_demand else {},
                "machinery": json.loads(r.machinery) if r.machinery else [],
                "skills_required": json.loads(r.skills_required) if r.skills_required else [],
                "schemes": json.loads(r.schemes) if r.schemes else [],
                "implementation_steps": json.loads(r.implementation_steps) if r.implementation_steps else []
            }
        except Exception as e:
            print(f"Error parsing blueprint JSON for {business_id}: {e}")
            return None
