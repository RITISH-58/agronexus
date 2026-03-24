from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, Any
from app.db.database import get_db
from app.services.business_service import BusinessService
from app.models.crop_business_model import CropBusinessDataset
from app.schemas.crop_business_schemas import CropBusinessResponse, CropBusinessListResponse
import json
from sqlalchemy import or_

router = APIRouter(tags=["Agribusiness Blueprint"])
business_service = BusinessService()

@router.get("/business/search")
def search_blueprints(
    q: Optional[str] = Query(None, description="Search query e.g. food processing, tomato, etc."),
    db: Session = Depends(get_db)
):
    try:
        return business_service.search_businesses(db, query=q)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/business/details/{business_id}")
def get_blueprint_details(
    business_id: int,
    db: Session = Depends(get_db)
):
    try:
        details = business_service.get_business_details(db, business_id=business_id)
        if not details:
            raise HTTPException(status_code=404, detail="Blueprint not found")
        return details
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- DYNAMIC CROP-TO-BUSINESS GENERATOR ENDPOINTS ---

@router.get("/business/generate", response_model=CropBusinessListResponse)
def generate_crop_businesses(crop: str, db: Session = Depends(get_db)):
    """Generate business blueprints based on crop search."""
    search_term = f"%{crop.strip().lower()}%"
    
    # Search simulated dataset dynamically
    results = db.query(CropBusinessDataset).filter(
        or_(
            CropBusinessDataset.crop_name.ilike(search_term),
            CropBusinessDataset.processed_product.ilike(search_term),
            CropBusinessDataset.industry_type.ilike(search_term)
        )
    ).all()
    
    businesses = []
    for r in results:
        try:
            businesses.append(
                CropBusinessResponse(
                    id=r.id,
                    crop_name=r.crop_name,
                    processed_product=r.processed_product,
                    industry_type=r.industry_type,
                    demand_level=r.demand_level,
                    industry_growth_rate=r.industry_growth_rate,
                    investment_range=r.investment_range,
                    roi_range=r.roi_range,
                    monthly_revenue=r.monthly_revenue,
                    profit_margin=r.profit_margin,
                    break_even=r.break_even,
                    investment_breakdown=json.loads(r.investment_breakdown) if r.investment_breakdown else {},
                    raw_material_req=json.loads(r.raw_material_req) if r.raw_material_req else {},
                    production_capacity=json.loads(r.production_capacity) if r.production_capacity else {},
                    revenue_projection=json.loads(r.revenue_projection) if r.revenue_projection else {},
                    market_demand=json.loads(r.market_demand) if r.market_demand else {},
                    machinery=json.loads(r.machinery) if r.machinery else [],
                    skills_required=json.loads(r.skills_required) if r.skills_required else [],
                    schemes=json.loads(r.schemes) if r.schemes else [],
                    implementation_steps=json.loads(r.implementation_steps) if r.implementation_steps else []
                )
            )
        except Exception as err:
            print(f"Error parsing JSON for object {r.id}: {err}")
            
    return CropBusinessListResponse(businesses=businesses)

@router.get("/business/blueprint/{id}", response_model=CropBusinessResponse)
def get_crop_blueprint(id: int, db: Session = Depends(get_db)):
    """Fetch complete 10-section blueprint for a generated business."""
    r = db.query(CropBusinessDataset).filter(CropBusinessDataset.id == id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Blueprint not found")
        
    try:
        return CropBusinessResponse(
            id=r.id,
            crop_name=r.crop_name,
            processed_product=r.processed_product,
            industry_type=r.industry_type,
            demand_level=r.demand_level,
            industry_growth_rate=r.industry_growth_rate,
            investment_range=r.investment_range,
            roi_range=r.roi_range,
            monthly_revenue=r.monthly_revenue,
            profit_margin=r.profit_margin,
            break_even=r.break_even,
            investment_breakdown=json.loads(r.investment_breakdown) if r.investment_breakdown else {},
            raw_material_req=json.loads(r.raw_material_req) if r.raw_material_req else {},
            production_capacity=json.loads(r.production_capacity) if r.production_capacity else {},
            revenue_projection=json.loads(r.revenue_projection) if r.revenue_projection else {},
            market_demand=json.loads(r.market_demand) if r.market_demand else {},
            machinery=json.loads(r.machinery) if r.machinery else [],
            skills_required=json.loads(r.skills_required) if r.skills_required else [],
            schemes=json.loads(r.schemes) if r.schemes else [],
            implementation_steps=json.loads(r.implementation_steps) if r.implementation_steps else []
        )
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))
