"""
Authentication and token verification
"""
from fastapi import HTTPException, status
from app.core.supabase import supabase


async def verify_token(token: str) -> dict:
    """
    Verify Supabase JWT token and return user data
    
    Args:
        token: JWT token from Authorization header
        
    Returns:
        User dict with id, email, etc.
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        # Verify token with Supabase and get user
        response = supabase.auth.get_user(token)
        
        if not response or not response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Extract user data
        user = response.user
        return {
            "id": user.id,
            "email": user.email,
            "aud": user.aud,
            "role": user.role
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
        
    except Exception as e:
        # Handle any Supabase errors
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token verification failed: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"}
        )
