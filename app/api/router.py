"""
Main API router - combines all endpoint routers
"""
from fastapi import APIRouter
from app.api.endpoints import auth, health, device, links


api_router = APIRouter()

# Public endpoints (no auth)
api_router.include_router(
    health.router,
    tags=["health"]
)

# Auth endpoints
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["auth"]
)

# Protected endpoints (require auth)
# api_router.include_router(
#     device.router,
#     prefix="/devices",
#     tags=["devices"]
# )

# api_router.include_router(
#     links.router,
#     prefix="/links",
#     tags=["links"]
# )
