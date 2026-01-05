from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TransactionCreate(BaseModel):
    user_id: str
    wallet_id: str
    parking_lot_id: str


class TransactionUpdate(BaseModel):
    end_time: Optional[datetime] = None
    duration: Optional[float] = None
    total_price: Optional[float] = None


class TransactionResponse(BaseModel):
    id: str
    user_id: str
    wallet_id: str
    parking_lot_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    price_id: str
    duration: Optional[float] = None
    total_price: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True
