from fastapi import APIRouter
from controllers.vehicle_type_controller import VehicleTypeController
from schemas.vehicle_type_schema import VehicleTypeCreate, VehicleTypeUpdate, VehicleTypeResponse

router = APIRouter(prefix="/vehicle-types", tags=["Vehicle Types"])

@router.post("/", response_model=VehicleTypeResponse)
async def add_type(type_data: VehicleTypeCreate):
    return await VehicleTypeController.add_type(type_data)

@router.get("/", response_model=list[VehicleTypeResponse])
async def get_all_types():
    return await VehicleTypeController.get_all_types()

@router.get("/{type_id}", response_model=VehicleTypeResponse)
async def get_type_by_id(type_id: str):
    return await VehicleTypeController.get_type_by_id(type_id)

@router.put("/{type_id}", response_model=VehicleTypeResponse)
async def update_type(type_id: str, type_data: VehicleTypeUpdate):
    return await VehicleTypeController.update_type(type_id, type_data)

@router.delete("/by-name/{name}")
async def delete_type_by_name(name: str):
    return await VehicleTypeController.delete_type_by_name(name)