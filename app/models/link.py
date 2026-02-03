from pydantic import BaseModel, HttpUrl, Field, field_validator
from typing import Optional
from datetime import datetime


class LinkCreate(BaseModel):
    device_id: str
    url: HttpUrl
    title: Optional[str] = None
    favicon_url: Optional[HttpUrl] = None

    @field_validator('url')
    def validate_url(cls, v):
        url_str = str(v)
        if len(url_str) > 2048:
            raise ValueError('URL too long')
        return v


class LinkResponse(BaseModel):
    id: str
    user_id: str
    device_id: str
    url: str
    status: str
    created_at: datetime
    title: Optional[str] = None
    favicon_url: Optional[str] = None


class LinkAcknowledge(BaseModel):
    status: str = 'acknowledged'

    @field_validator('status')
    def validate_status(cls, v):
        if v not in ['acknowledged', 'failed']:
            raise ValueError('Invalid status')
        return v


class PendingLinksQuery(BaseModel):
    device_id: str
    limit: int = 50

    @field_validator('limit')
    def validate_limit(cls, v):
        if v > 100:
            raise ValueError('Maximum 100 links per request')
        return v