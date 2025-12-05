from pydantic import BaseModel
from typing import Optional

class VehicleCreate(BaseModel):
    user_id: str
    license_plate: str
    type_id: str

class VehicleUpdate(BaseModel):
    license_plate: Optional[str]
    type_id: Optional[str]

class VehicleResponse(BaseModel):
    id: str
    user_id: str
    license_plate: str
    type_id: str