# models/parking.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class User(BaseModel):
    id: str = Field(alias="_id")
    name: str
    phone: str
    password: str
    role: str
    balance: float = 0.0

class ParkingLot(BaseModel):
    id: str = Field(alias="_id")
    name: str
    status: str # "available", "occupied"

class Invoice(BaseModel):
    id: str = Field(alias="_id")
    user_id: str
    plot_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    unit_price: float
    duration: float = 0.0
    total_price: float = 0.0