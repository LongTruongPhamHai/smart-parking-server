from pydantic import BaseModel
from typing import Optional

class WalletCreate(BaseModel):
    user_id: str
    name: str = "My wallet"

class WalletResponse(BaseModel):
    id: str
    user_id: str
    name: str
    balance: float

class WalletFund(BaseModel):
    amount: float

class WalletPayment(BaseModel):
    amount: float