from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
import math
import json
from app.db.database import get_db
from app.models.extra_venture_models import BuyerDirectory, SuccessStory
from app.schemas.extra_venture_schemas import (
    BuyerResponse, BuyerListResponse,
    SuccessStoryResponse, SuccessStoryListResponse
)

router = APIRouter(tags=["Extra Venture Tools (Buyers & Success Stories)"])

def haversine(lat1, lon1, lat2, lon2):
    """Calculate the great circle distance between two points on the earth."""
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371
    return c * r

# ==============================
# BUYER ENDPOINTS
# ==============================
@router.get("/buyers", response_model=BuyerListResponse)
def get_buyers(
    product: Optional[str] = None,
    location: Optional[str] = None,
    lat: Optional[float] = None,
    lng: Optional[float] = None,
    radius_km: float = 100.0,
    page: int = 1,
    per_page: int = 50,
    db: Session = Depends(get_db)
):
    query = db.query(BuyerDirectory)
    
    if product:
        search_term = f"%{product.strip().lower()}%"
        query = query.filter(
            or_(
                BuyerDirectory.product_category.ilike(search_term),
                BuyerDirectory.buyer_name.ilike(search_term)
            )
        )
    
    if location and not lat and not lng:
        loc_term = f"%{location.strip().lower()}%"
        query = query.filter(
            or_(
                BuyerDirectory.city.ilike(loc_term),
                BuyerDirectory.state.ilike(loc_term),
                BuyerDirectory.district.ilike(loc_term)
            )
        )
        
    results = query.all()
    
    responses = []
    for b in results:
        dist = None
        if lat is not None and lng is not None and b.latitude and b.longitude:
            dist = haversine(lat, lng, b.latitude, b.longitude)
            if dist > radius_km:
                continue
        
        responses.append(
            BuyerResponse(
                id=b.id,
                buyer_name=b.buyer_name,
                business_type=b.business_type or "",
                product_category=b.product_category or "",
                annual_capacity=b.annual_capacity,
                city=b.city or "",
                district=b.district,
                state=b.state or "",
                latitude=b.latitude or 0.0,
                longitude=b.longitude or 0.0,
                phone_number=b.phone_number or "",
                email=b.email or "",
                website=b.website,
                buyer_description=b.buyer_description,
                distance_km=round(dist, 1) if dist is not None else None
            )
        )
        
    responses.sort(key=lambda x: x.distance_km if x.distance_km is not None else 999999)
    
    total = len(responses)
    start = (page - 1) * per_page
    end = start + per_page
    paginated = responses[start:end]
    
    return BuyerListResponse(buyers=paginated, total=total, page=page, per_page=per_page)

@router.get("/buyers/search", response_model=BuyerListResponse)
def search_buyers(
    product: Optional[str] = None,
    location: Optional[str] = None,
    page: int = 1,
    per_page: int = 50,
    db: Session = Depends(get_db)
):
    """Search buyers by product and/or location with pagination."""
    query = db.query(BuyerDirectory)
    
    if product and product.strip():
        search_term = f"%{product.strip().lower()}%"
        query = query.filter(
            or_(
                BuyerDirectory.product_category.ilike(search_term),
                BuyerDirectory.buyer_name.ilike(search_term),
                BuyerDirectory.business_type.ilike(search_term)
            )
        )
    
    if location and location.strip():
        loc_term = f"%{location.strip().lower()}%"
        query = query.filter(
            or_(
                BuyerDirectory.city.ilike(loc_term),
                BuyerDirectory.state.ilike(loc_term),
                BuyerDirectory.district.ilike(loc_term)
            )
        )
    
    total = query.count()
    offset = (page - 1) * per_page
    results = query.offset(offset).limit(per_page).all()
    
    responses = []
    for b in results:
        responses.append(
            BuyerResponse(
                id=b.id,
                buyer_name=b.buyer_name,
                business_type=b.business_type or "",
                product_category=b.product_category or "",
                annual_capacity=b.annual_capacity,
                city=b.city or "",
                district=b.district,
                state=b.state or "",
                latitude=b.latitude or 0.0,
                longitude=b.longitude or 0.0,
                phone_number=b.phone_number or "",
                email=b.email or "",
                website=b.website,
                buyer_description=b.buyer_description,
            )
        )
    
    return BuyerListResponse(buyers=responses, total=total, page=page, per_page=per_page)

@router.get("/buyers/{buyer_id}", response_model=BuyerResponse)
def get_buyer_profile(buyer_id: int, db: Session = Depends(get_db)):
    """Get full buyer profile by ID."""
    b = db.query(BuyerDirectory).filter(BuyerDirectory.id == buyer_id).first()
    if not b:
        raise HTTPException(status_code=404, detail="Buyer not found")
    
    return BuyerResponse(
        id=b.id,
        buyer_name=b.buyer_name,
        business_type=b.business_type or "",
        product_category=b.product_category or "",
        annual_capacity=b.annual_capacity,
        city=b.city or "",
        district=b.district,
        state=b.state or "",
        latitude=b.latitude or 0.0,
        longitude=b.longitude or 0.0,
        phone_number=b.phone_number or "",
        email=b.email or "",
        website=b.website,
        buyer_description=b.buyer_description,
    )

@router.get("/buyers/suggestions")
def get_buyer_suggestions(q: str = "", db: Session = Depends(get_db)):
    """Return quick suggestions for autocomplete."""
    if not q or len(q) < 2:
        return {"suggestions": []}
    
    term = f"%{q.strip().lower()}%"
    products = db.query(BuyerDirectory.product_category).filter(
        BuyerDirectory.product_category.ilike(term)
    ).distinct().limit(5).all()
    cities = db.query(BuyerDirectory.city).filter(
        BuyerDirectory.city.ilike(term)
    ).distinct().limit(5).all()
    
    suggestions = []
    for p in products:
        suggestions.append({"type": "product", "value": p[0]})
    for c in cities:
        suggestions.append({"type": "location", "value": c[0]})
    
    return {"suggestions": suggestions}


# ==============================
# SUCCESS STORIES ENDPOINTS
# ==============================

def _parse_json_field(val):
    """Safely parse a JSON field, return empty list on failure."""
    if not val:
        return []
    try:
        return json.loads(val)
    except Exception:
        return []

def _story_to_response(s):
    """Convert a SuccessStory ORM object to a response dict."""
    return SuccessStoryResponse(
        id=s.id,
        farmer_name=s.farmer_name,
        state=s.state or "",
        district=s.district,
        crop=s.crop or "",
        business_type=s.business_type or "",
        investment=s.investment or "",
        monthly_income=s.monthly_income or "",
        yearly_income=s.yearly_income or "",
        products_sold=_parse_json_field(s.products_sold),
        buyers_connected=_parse_json_field(s.buyers_connected),
        government_scheme_used=s.government_scheme_used,
        implementation_steps=_parse_json_field(s.implementation_steps),
        story=s.story,
        contact_phone=s.contact_phone,
        contact_email=s.contact_email,
    )

@router.get("/success-stories", response_model=SuccessStoryListResponse)
def get_success_stories(
    crop: Optional[str] = None,
    state: Optional[str] = None,
    page: int = 1,
    per_page: int = 20,
    db: Session = Depends(get_db)
):
    """List success stories with optional crop and state filters, paginated."""
    query = db.query(SuccessStory)
    
    if crop and crop.strip():
        crop_term = f"%{crop.strip().lower()}%"
        query = query.filter(
            or_(
                SuccessStory.crop.ilike(crop_term),
                SuccessStory.business_type.ilike(crop_term)
            )
        )
    
    if state and state.strip():
        state_term = f"%{state.strip().lower()}%"
        query = query.filter(SuccessStory.state.ilike(state_term))
    
    total = query.count()
    offset = (page - 1) * per_page
    results = query.offset(offset).limit(per_page).all()
    
    responses = [_story_to_response(s) for s in results]
    return SuccessStoryListResponse(stories=responses, total=total, page=page, per_page=per_page)

@router.get("/success-stories/{story_id}", response_model=SuccessStoryResponse)
def get_success_story_detail(story_id: int, db: Session = Depends(get_db)):
    """Get full success story by ID."""
    s = db.query(SuccessStory).filter(SuccessStory.id == story_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Success story not found")
    return _story_to_response(s)
