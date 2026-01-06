from pydantic import BaseModel
from typing import Optional


class ParkingLotCreate(BaseModel):
    name: str
    unit_price: float


class ParkingLotUpdate(BaseModel):
    name: Optional[str] = None
    unit_price: Optional[float] = None
    status: Optional[str] = None  # 'available' hoặc 'occupied'


class ParkingLotResponse(BaseModel):
    id: str
    name: str
    unit_price: float
    status: str

    class Config:
        from_attributes = True
