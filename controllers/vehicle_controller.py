from fastapi import HTTPException
from services.vehicle_service import VehicleService
from schemas.vehicle_schema import VehicleCreate, VehicleUpdate, VehicleResponse

class VehicleController:
    @staticmethod
    async def add_vehicle(vehicle: VehicleCreate) -> VehicleResponse:
        new_vehicle = await VehicleService.add_vehicle(vehicle)
        return VehicleResponse(**new_vehicle.to_dict())

    @staticmethod
    async def get_all_vehicles() -> list[VehicleResponse]:
        vehicles = await VehicleService.get_all_vehicles()
        return [VehicleResponse(**v.to_dict()) for v in vehicles]

    @staticmethod
    async def get_vehicle_by_id(vehicle_id: str) -> VehicleResponse:
        vehicle = await VehicleService.get_vehicle_by_id(vehicle_id)
        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        return VehicleResponse(**vehicle.to_dict())

    @staticmethod
    async def get_vehicles_by_user_id(user_id: str) -> list[VehicleResponse]:
        vehicles = await VehicleService.get_vehicles_by_user_id(user_id)
        return [VehicleResponse(**v.to_dict()) for v in vehicles]

    @staticmethod
    async def update_vehicle(vehicle_id: str, vehicle: VehicleUpdate) -> VehicleResponse:
        updated = await VehicleService.update_vehicle(vehicle_id, vehicle)
        if not updated:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        return VehicleResponse(**updated.to_dict())

    @staticmethod
    async def delete_vehicle(vehicle_id: str) -> dict:
        deleted = await VehicleService.delete_vehicle(vehicle_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        return {"message": "Vehicle deleted successfully"}