from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserSignup(BaseModel):
    name: str
    email: EmailStr
    phone: str
    password: str

class UserSignin(BaseModel):
    phone: str
    password: str

class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    password: Optional[str]
    role: Optional[str]

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    phone: str
    role: str
    created_at: datetime
    updated_at: datetime