from fastapi import HTTPException
from services.vehicle_type_service import VehicleTypeService
from schemas.vehicle_type_schema import VehicleTypeCreate, VehicleTypeUpdate, VehicleTypeResponse

class VehicleTypeController:
    @staticmethod
    async def add_type(type_data: VehicleTypeCreate) -> VehicleTypeResponse:
        new_type = await VehicleTypeService.add_type(type_data.name)
        return VehicleTypeResponse(**new_type.to_dict())

    @staticmethod
    async def get_all_types() -> list[VehicleTypeResponse]:
        types = await VehicleTypeService.get_all_types()
        return [VehicleTypeResponse(**t.to_dict()) for t in types]

    @staticmethod
    async def get_type_by_id(type_id: str) -> VehicleTypeResponse:
        type_data = await VehicleTypeService.get_type_by_id(type_id)
        if not type_data:
            raise HTTPException(status_code=404, detail="Type not found")
        return VehicleTypeResponse(**type_data.to_dict())

    @staticmethod
    async def update_type(type_id: str, type_data: VehicleTypeUpdate) -> VehicleTypeResponse:
        updated = await VehicleTypeService.update_type(type_id, type_data.name)
        if not updated:
            raise HTTPException(status_code=404, detail="Type not found")
        return VehicleTypeResponse(**updated.to_dict())

    @staticmethod
    async def delete_type_by_name(name: str) -> dict:
        deleted = await VehicleTypeService.delete_type_by_name(name)
        if not deleted:
            raise HTTPException(status_code=404, detail="Type not found")
        return {"message": "Vehicle type deleted successfully"}