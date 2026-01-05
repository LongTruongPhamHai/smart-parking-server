from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ParkingLotCreate(BaseModel):
    name: str
    unit_price: float


class ParkingLotUpdate(BaseModel):
    name: Optional[str] = None
    unit_price: Optional[float] = None


class ParkingLotResponse(BaseModel):
    id: str
    name: str
    unit_price: float
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
