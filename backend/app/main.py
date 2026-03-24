from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Import endpoints module only for its side-effect of creating DB tables
import app.api.endpoints  # noqa: F401
from app.api.scheme_routes import router as scheme_router
from app.api.crop_routes import router as crop_router
from app.api.business_routes import router as business_router
from app.api.auth_routes import router as auth_router
from app.api.profile_routes import router as profile_router
from app.api.weather_routes import router as weather_router
import os

app = FastAPI(title="AgroNexus AI API", version="2.0.0")

# CORS Configuration — allow all origins during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(scheme_router, prefix="/api", tags=["Government Schemes"])
app.include_router(crop_router, prefix="/api", tags=["Crop Intelligence"])
app.include_router(business_router, prefix="/api", tags=["Agribusiness"])
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(profile_router, prefix="/api", tags=["Profile & Land"])
app.include_router(weather_router, prefix="/api", tags=["Weather Intelligence"])
from app.api.extra_venture_routes import router as extra_venture_router
app.include_router(extra_venture_router, prefix="/api", tags=["Buyers & Stories"])
from app.api.venture_routes import router as venture_router
app.include_router(venture_router, prefix="/api", tags=["Smart Venture Planner"])



@app.get("/")
def read_root():
    return {"message": "Welcome to AgroNexus AI API"}

@app.on_event("startup")
def startup_seed():
    """Seed agri business data and extra venture data on startup if tables are empty."""
    try:
        from app.data.seed_agri_business import run_seed as seed_agri
        seed_agri()
        
        from app.data.seed_extra_venture_data import run_seed as seed_extra
        seed_extra()
        
        from app.data.seed_crop_business_dataset import run_seed as seed_crop
        seed_crop()
        
        from app.data.seed_buyers_india import run_seed as seed_buyers
        seed_buyers()
        
        from app.data.seed_success_stories import run_seed as seed_stories
        seed_stories()
        
        from app.data.seed_agri_ventures import run_seed as seed_ventures
        seed_ventures()
    except Exception as e:
        print(f"Seed warning: {e}")
