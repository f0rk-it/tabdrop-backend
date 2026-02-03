from fastapi import APIRouter, Depends, HTTPException, status
from app.api.deps import get_current_user
from app.models.user import User
from app.models.device import DeviceCreate, DeviceUpdate, DeviceResponse
from app.core.supabase import supabase
from typing import List
from datetime import datetime

router = APIRouter()

@router.post('/register', response_model=DeviceResponse, status_code=201)
async def register_device(
        device_data: DeviceCreate,
        current_user: User = Depends(get_current_user)
):
    existing = supabase.table('devices') \
        .select('*') \
        .eq('user_id', current_user.id) \
        .eq('device_name', device_data.device_name) \
        .execute()
    
    if existing.data:
        raise HTTPException(409, 'Device name already exists')
    
    result = supabase.table('devices').insert({
        'user_id': current_user.id,
        'device_name': device_data.device_name,
        'device_type': device_data.device_type,
        'last_seen': datetime.utcnow()
    }).execute()

    return result.data[0]

@router.get('', response_model=List[DeviceResponse])
async def list_devices(
    current_user: User = Depends(get_current_user)
):
    result = supabase.table('devices') \
        .select('*') \
        .eq('user_id', current_user.id) \
        .order('last_seen', desc=True) \
        .execute()
    
    return result.data

@router.patch('/{device_id}', response_model=DeviceResponse)
async def update_device(
    device_id: str,
    device_data: DeviceUpdate,
    current_user: User = Depends(get_current_user)
):
    device = supabase.table('devices') \
        .select('*') \
        .eq('id', device_id) \
        .eq('user_id', current_user.id) \
        .single() \
        .execute()
    
    if not device.data:
        raise HTTPException(404, 'Device not found')
    
    result = supabase.table('devices') \
        .update({'device_name': device_data.device_name}) \
        .eq('id', device_id) \
        .execute()
    
    return result.data[0]

@router.delete('/{device_id}')
async def delete_device(
    device_id: str,
    current_user: User = Depends(get_current_user)
):
    result = supabase.table('devices') \
        .delete() \
        .eq('id', device_id) \
        .eq('user_id', current_user.id) \
        .execute()
    
    if not result.data:
        raise HTTPException(404, 'Device not found')
    
    return {'message': 'Device deleted successfully'}