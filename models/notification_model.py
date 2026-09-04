from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class NotificationModel(BaseModel):
    """Model cho Notification trong MongoDB"""
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str  # ID của user nhận thông báo
    title: str  # Tiêu đề thông báo
    message: str  # Nội dung thông báo
    type: str  # Loại: 'info', 'warning', 'success', 'error', 'fire', 'gas'
    is_read: bool = False  # Đã đọc hay chưa
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}
