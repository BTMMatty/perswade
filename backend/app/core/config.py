import os
from functools import lru_cache

class Settings:
    """Application settings"""
    
    # API Keys
    assemblyai_api_key: str = os.getenv("ASSEMBLYAI_API_KEY", "")
    
    # App Config
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    
    # Security
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-here")

@lru_cache()
def get_settings():
    return Settings()
