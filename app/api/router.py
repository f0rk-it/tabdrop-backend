from fastapi import APIRouter
from app.config import settings
from app.api.endpoints import auth, device, health, links


router = APIRouter()


@router.get('/health', tags=['Health'])
async def health_check():
    """
    Health check endpoint to verify that the API is running
    """
    return {
        'status': 'healthy',
        'app_name': settings.APP_NAME,
        'environment': settings.ENV
    }
