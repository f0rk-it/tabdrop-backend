"""
env vars and settings management
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # App
    APP_NAME: str = 'TabDrop Backend'
    ENV: str = 'development'  # development | production

    # Frontend
    FRONTEND_ORIGINS: List[str] = [
        'http://localhost:3000',
        'https://tabdrop.vercel.app',
    ]

    # Supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str


    class Config:
        env_file = '.env'
        case_sensitive = True


settings = Settings()