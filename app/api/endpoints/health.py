"""
Health check endpoint (no auth required)
"""
from fastapi import APIRouter


router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Health check endpoint - returns API status
    
    No authentication required.
    Used for monitoring and deployment verification.
    """
    return {
        "status": "healthy",
        "service": "TabDrop Backend API"
    }
