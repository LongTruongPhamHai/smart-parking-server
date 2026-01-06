from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class InvoiceCreate(BaseModel):
    user_id: str
    unit_price: float


class InvoiceResponse(BaseModel):
    id: str
    user_id: str
    start_time: datetime
    end_time: Optional[datetime]
    unit_price: float
    duration: float
    total_price: float
    status: str

    class Config:
        from_attributes = True
