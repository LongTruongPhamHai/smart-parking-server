from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserSignup(BaseModel):
    name: str
    phone: str
    email: str
    password: str


class UserSignin(BaseModel):
    phone: str
    password: str


class UserUpdate(BaseModel):
    name: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    password: Optional[str]
    role: Optional[str]
    balance: Optional[float]


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    phone: str
    role: str
    balance: float
