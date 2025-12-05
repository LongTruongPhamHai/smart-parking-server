from fastapi import APIRouter
from controllers.vehicle_controller import VehicleController
from schemas.vehicle_schema import VehicleCreate, VehicleUpdate, VehicleResponse

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])

@router.post("/", response_model=VehicleResponse)
async def add_vehicle(vehicle: VehicleCreate):
    return await VehicleController.add_vehicle(vehicle)

@router.get("/", response_model=list[VehicleResponse])
async def get_all_vehicles():
    return await VehicleController.get_all_vehicles()

@router.get("/{vehicle_id}", response_model=VehicleResponse)
async def get_vehicle_by_id(vehicle_id: str):
    return await VehicleController.get_vehicle_by_id(vehicle_id)

@router.get("/by-user/{user_id}", response_model=list[VehicleResponse])
async def get_vehicles_by_user_id(user_id: str):
    return await VehicleController.get_vehicles_by_user_id(user_id)

@router.put("/{vehicle_id}", response_model=VehicleResponse)
async def update_vehicle(vehicle_id: str, vehicle: VehicleUpdate):
    return await VehicleController.update_vehicle(vehicle_id, vehicle)

@router.delete("/{vehicle_id}")
async def delete_vehicle(vehicle_id: str):
    return await VehicleController.delete_vehicle(vehicle_id)