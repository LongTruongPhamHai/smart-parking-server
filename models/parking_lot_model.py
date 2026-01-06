# models/parking_lot.py
from pydantic import BaseModel, Field
from typing import Optional


class ParkingLot(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    name: str
    status: str = "Trống"  # Trống, Đã đặt, Đang sử dụng
