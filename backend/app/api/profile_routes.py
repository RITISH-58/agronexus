from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas import user as schemas
from app.models import user as user_models
from app.models import land_model
from app.core import security

router = APIRouter()

@router.put("/profile/update", response_model=schemas.User)
def update_profile(
    profile_data: schemas.UserUpdate, 
    current_user: user_models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    if profile_data.full_name is not None:
        current_user.full_name = profile_data.full_name
    if profile_data.phone is not None:
        current_user.phone = profile_data.phone
    if profile_data.state is not None:
        current_user.state = profile_data.state
    if profile_data.district is not None:
        current_user.district = profile_data.district
        
    db.commit()
    db.refresh(current_user)
    return current_user

@router.post("/profile/land", response_model=schemas.LandDetailResponse)
def add_land(
    land_data: schemas.LandDetailCreate,
    current_user: user_models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    new_land = land_model.LandDetail(
        **land_data.dict(),
        user_id=current_user.id
    )
    db.add(new_land)
    db.commit()
    db.refresh(new_land)
    return new_land

@router.get("/profile/land", response_model=List[schemas.LandDetailResponse])
def get_land_details(
    current_user: user_models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    lands = db.query(land_model.LandDetail).filter(land_model.LandDetail.user_id == current_user.id).all()
    return lands

@router.delete("/profile/land/{land_id}")
def delete_land(
    land_id: int,
    current_user: user_models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    land = db.query(land_model.LandDetail).filter(
        land_model.LandDetail.land_id == land_id,
        land_model.LandDetail.user_id == current_user.id
    ).first()
    
    if not land:
        raise HTTPException(status_code=404, detail="Land detail not found")
        
    db.delete(land)
    db.commit()
    return {"message": "Land detail deleted successfully"}
