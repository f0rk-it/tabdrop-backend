from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.api.deps import get_current_user
from app.models.user import User
from app.models.link import LinkCreate, LinkResponse, LinkAcknowledge
from app.core.supabase import supabase
from typing import List
from datetime import datetime, timedelta

router = APIRouter()

@router.post('/send', response_model=LinkResponse, status_code=201)
async def send_link(
    link_data: LinkCreate,
    current_user: User = Depends(get_current_user)
):
    device = supabase.table('devices') \
        .select('*') \
        .eq('id', link_data.device_id) \
        .eq('user_id', current_user.id) \
        .single() \
        .execute()
    
    if not device.data:
        raise HTTPException(
            status_code=404,
            detail='Device not found or does not belong to you'
        )
    
    result = supabase.table('links').insert({
        'user_id': current_user.id,
        'device_id': link_data.device_id,
        'url': str(link_data.url),
        'status': 'pending',
        'title': link_data.title,
        'favicon_url': str(link_data.favicon_url) if link_data.favicon_url else None,
    }).execute()

    return result.data[0]

@router.get('/pending', response_model=List[LinkResponse])
async def get_pending_links(
    device_id: str = Query(..., description='Device ID to get links for'),
    current_user: User = Depends(get_current_user)
):
    device = supabase.table('devices') \
        .select('id') \
        .eq('id', device_id) \
        .eq('user_id', current_user.id) \
        .single() \
        .execute()
    
    if not device.data:
        raise HTTPException(
            status_code=404,
            detail='Device not found'
        )
    
    pending = supabase.table('links') \
        .select('*') \
        .eq('device_id', device_id) \
        .eq('status', 'pending') \
        .order('created_at', desc=False) \
        .execute()
    
    links = pending.data

    if links:
        link_ids = [link['id'] for link in links]

        supabase.table('links') \
            .update({
                'status': 'delivered',
                'delivered_at': datetime.utcnow().isoformat()
            }) \
            .in_('id', link_ids) \
            .execute()
        
        for link in links:
            link['status'] = 'delivered'
            link['delivered_at'] = datetime.utcnow().isoformat()
    
    return links

@router.post('/{link_id}/acknowledge', response_model=LinkResponse)
async def acknowledge_link(
    link_id: str,
    ack_data: LinkAcknowledge,
    current_user: User = Depends(get_current_user)
):
    link = supabase.table('links') \
        .select('*') \
        .eq('id', link_id) \
        .eq('user_id', current_user.id) \
        .single() \
        .execute()
    
    if not link.data:
        raise HTTPException(
            status_code=404,
            detail='Link not found'
        )
    
    if link.data['status'] == 'acknowledged':
        return link.data
    
    result = supabase.table('links') \
        .update({
            'status': ack_data.status,
            'acknowledged_at': datetime.utcnow().isoformat()
        }) \
        .eq('id', link_id) \
        .execute()
    
    return result.data[0]

@router.get('/history', response_model=List[LinkResponse])
async def get_link_history(
    limit: int =  Query(50, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user)
):
    result = supabase.table('links') \
        .select('*') \
        .eq('user_id', current_user.id) \
        .order('created_at', desc=True) \
        .range(offset, offset + limit - 1) \
        .execute()
    
    return result.data