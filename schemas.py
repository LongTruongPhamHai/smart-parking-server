# schemas/invoice_schema.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class InvoiceCreate(BaseModel):
    user_id: str
    plot_id: str
    unit_price: float


class InvoiceResponse(BaseModel):
    id: str
    total_price: float
    status: str
