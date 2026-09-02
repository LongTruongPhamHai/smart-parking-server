from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserSignup(BaseModel):
    name: str
    phone: str
    email: str
    password: str


class UserCreateAdmin(BaseModel):
    name: str
    phone: str
    email: str
    password: str
    role: str
    balance: float = 0.0


class UserSignin(BaseModel):
    phone: str
    password: str


class CheckInRequest(UserSignin):
    parking_lot_id: Optional[str] = None


class UserChangePassword(BaseModel):
    old_password: str
    new_password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    balance: Optional[float] = None


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    phone: str
    role: str
    balance: float
