from pydantic import BaseModel

class VehicleTypeCreate(BaseModel):
    name: str

class VehicleTypeUpdate(BaseModel):
    name: str

class VehicleTypeResponse(BaseModel):
    id: str
    name: str