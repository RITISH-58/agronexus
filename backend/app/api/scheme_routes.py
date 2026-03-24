from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db, engine
from app.models import scheme_model
from app.schemas import scheme_schema
from app.services.scheme_service import SchemeService
import logging

scheme_model.Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/scheme-recommendation", tags=["Government Schemes"])
logger = logging.getLogger(__name__)

def get_scheme_service(db: Session = Depends(get_db)):
    return SchemeService(db)

@router.post("", response_model=scheme_schema.SchemeRecommendationResponse)
def get_scheme_recommendation(
    request: scheme_schema.SchemeRecommendationRequest,
    service: SchemeService = Depends(get_scheme_service)
):
    """
    Recommend government schemes based on farmer input (soil, land, location).
    """
    try:
        response_data = service.get_scheme_recommendations(request)
        return response_data
    except Exception as e:
        logger.error(f"Error in scheme recommendation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching scheme recommendations."
        )
