from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserSignup(BaseModel):
    name: str
    phone: str
    password: str


class UserSignin(BaseModel):
    phone: str
    password: str


class UserUpdate(BaseModel):
    name: Optional[str]
    phone: Optional[str]
    password: Optional[str]
    role: Optional[str]
    balance: Optional[float]  # Thêm balance nếu muốn cập nhật số dư


class UserResponse(BaseModel):
    id: str
    name: str
    phone: str
    role: str
    balance: float  # Thêm balance
    created_at: datetime
    updated_at: datetime
