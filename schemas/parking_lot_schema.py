# schemas/parking_lot_schema.py
from pydantic import BaseModel
from typing import Optional


class ParkingLotCreate(BaseModel):
    name: str
    status: Optional[str] = "Trống"


class ParkingLotUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None


class ParkingLotResponse(BaseModel):
    id: str
    name: str
    status: str
