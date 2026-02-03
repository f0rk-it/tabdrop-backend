from pydantic import BaseModel, field_validator
from datetime import datetime


class DeviceCreate(BaseModel):
    device_name: str
    device_type: str

    @field_validator('device_type')
    def validate_device_type(cls, v):
        if v not in ['desktop', 'mobile']:
            raise ValueError('device_type must be either desktop or mobile')
        return v
    
    @field_validator('device_name')
    def clean_device_name(cls, v):
        return v.strip()[:100]
    

class DeviceUpdate(BaseModel):
    device_name: str


class DeviceResponse(BaseModel):
    id: str
    user_id: str
    device_name: str
    device_type: str
    last_seen: datetime
    created_at: datetime