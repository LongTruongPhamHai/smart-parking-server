from repositories.vehicle_type_repository import VehicleTypeRepository

class VehicleTypeService:
    @staticmethod
    async def add_type(name: str):
        return await VehicleTypeRepository.create(name)

    @staticmethod
    async def get_all_types():
        return await VehicleTypeRepository.get_all()

    @staticmethod
    async def get_type_by_id(type_id: str):
        return await VehicleTypeRepository.get_by_id(type_id)

    @staticmethod
    async def update_type(type_id: str, name: str):
        return await VehicleTypeRepository.update(type_id, name)

    @staticmethod
    async def delete_type_by_name(name: str):
        return await VehicleTypeRepository.delete_by_name(name)