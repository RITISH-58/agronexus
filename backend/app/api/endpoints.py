from app.db.database import engine
from app.models import user as models

# Also import LandDetail and CropPlan so they get created in DB
from app.models.land_model import LandDetail
from app.models.crop_plan import CropPlan

from app.models.agri_business_model import AgriBusiness
from app.models.extra_venture_models import BuyerDirectory, SuccessStory
from app.models.crop_business_model import CropBusinessDataset
from app.models.venture_model import AgriVentureDataset
from app.models.whatsapp import WhatsappMessage

# Create all database tables on import
models.Base.metadata.create_all(bind=engine)
