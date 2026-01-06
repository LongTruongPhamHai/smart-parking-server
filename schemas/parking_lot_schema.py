from pydantic import BaseModel
from typing import Optional


class ParkingLotCreate(BaseModel):
    name: str
    status: Optional[str] = "available"


class ParkingLotUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None


class ParkingLotResponse(BaseModel):
    id: str
    name: str
    status: str
