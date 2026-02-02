"""
FastAPI dependencies for auth and common utilities
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import verify_token
from app.models.user import User


# Security scheme for Swagger docs
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """
    Extract and verify JWT token from Authorization header
    
    Usage:
        @router.get("/protected")
        async def protected_route(current_user: User = Depends(get_current_user)):
            user_id = current_user.id
            # ... use user_id in your logic
    
    Args:
        credentials: HTTP Bearer token from request header
        
    Returns:
        User object with verified user data
        
    Raises:
        HTTPException: If token is missing, malformed, or invalid
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Extract token from credentials
    token = credentials.credentials
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization format",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Verify token and get user data
    user_data = await verify_token(token)
    
    # Convert to User model
    return User(**user_data)
