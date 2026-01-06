from pydantic import BaseModel, Field
from typing import Optional


class UserSignup(BaseModel):
    name: str
    phone: str
    password: str


class UserSignin(BaseModel):
    phone: str
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None


class UserUpdateBalance(BaseModel):
    balance: float


class UserResponse(BaseModel):
    id: str
    name: str
    phone: str
    role: str
    balance: float

    class Config:
        from_attributes = True
