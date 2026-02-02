"""
User-related Pydantic models
"""
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    """
    User model from Supabase auth
    """
    id: str
    email: EmailStr
    aud: str = "authenticated"
    role: str = "authenticated"
    
    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    """
    Public user data for API responses
    """
    id: str
    email: EmailStr
