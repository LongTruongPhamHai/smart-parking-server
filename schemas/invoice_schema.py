from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class InvoiceCreate(BaseModel):
    user_id: str
    parking_lot_id: str


class InvoiceResponse(BaseModel):
    id: str
    user_id: str
    parking_lot_id: str
    start_time: datetime
    end_time: Optional[datetime]
    duration: float
    total_price: float

    class Config:
        from_attributes = True
