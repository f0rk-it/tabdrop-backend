"""
CORS, logging and error handling middleware
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

def setup_middleware(app: FastAPI) -> None:
    # CORS - allow requests from frontend URLs
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.FRONTEND_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )