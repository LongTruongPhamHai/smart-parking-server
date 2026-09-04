from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class NotificationResponse(BaseModel):
    """Schema response cho notification"""
    id: str
    user_id: str
    title: str
    message: str
    type: str
    is_read: bool
    created_at: datetime


class NotificationCreate(BaseModel):
    """Schema để tạo notification cho 1 user"""
    user_id: str
    title: str
    message: str
    type: str = "info"


class NotificationBroadcast(BaseModel):
    """Schema để tạo notification broadcast cho nhiều users"""
    title: str
    message: str
    type: str = "info"
    target: str = "all"  # 'all' hoặc 'admins'
