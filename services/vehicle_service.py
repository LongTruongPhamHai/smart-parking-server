from repositories.vehicle_repository import VehicleRepository
from schemas.vehicle_schema import VehicleCreate, VehicleUpdate

class VehicleService:
    @staticmethod
    async def add_vehicle(vehicle: VehicleCreate):
        return await VehicleRepository.create(vehicle.dict())

    @staticmethod
    async def get_all_vehicles():
        return await VehicleRepository.get_all()

    @staticmethod
    async def get_vehicle_by_id(vehicle_id: str):
        return await VehicleRepository.get_by_id(vehicle_id)

    @staticmethod
    async def get_vehicles_by_user_id(user_id: str):
        return await VehicleRepository.get_by_user_id(user_id)

    @staticmethod
    async def update_vehicle(vehicle_id: str, vehicle: VehicleUpdate):
        return await VehicleRepository.update(vehicle_id, vehicle.dict(exclude_unset=True))

    @staticmethod
    async def delete_vehicle(vehicle_id: str):
        return await VehicleRepository.delete(vehicle_id)