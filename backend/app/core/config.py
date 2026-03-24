import os

class Settings:
    PROJECT_NAME: str = "AgroNexus AI"
    API_V1_STR: str = "/api"
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./agro_app.db")
    
settings = Settings()
