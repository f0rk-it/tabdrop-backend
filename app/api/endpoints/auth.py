"""
Authentication endpoints
"""
from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from app.models.user import User, UserResponse


router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user information
    
    Use this endpoint to:
    - Test if authentication is working
    - Get user details from token
    - Verify token validity
    
    Returns:
        User object with id and email
    """
    return UserResponse(
        id=current_user.id,
        email=current_user.email
    )
