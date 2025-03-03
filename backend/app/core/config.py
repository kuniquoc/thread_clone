from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache

class Settings(BaseSettings):
    # Base
    PROJECT_NAME: str = "Threads Clone"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "postgresql://admin:admin@localhost/threads"
    
    # Security
    SECRET_KEY: str = "con-so-gi-day"  # Change in production!
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    BACKEND_CORS_ORIGINS: list = [
        "http://localhost:3000",  # React development server
        "http://localhost:5173",  # Vite development server
        "https://your-production-frontend-domain.com"  # Add your production domain
    ]
    
    # Hugging Face
    HUGGING_FACE_API_TOKEN: Optional[str] = None
    
    class Config:
        case_sensitive = True
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()

# Create settings instance
settings = get_settings() 