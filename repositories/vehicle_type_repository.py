from db import db
from models.vehicle_type_model import VehicleTypeModel
from bson import ObjectId

class VehicleTypeRepository:
    collection = db["vehicle_types"]

    @staticmethod
    async def create(name: str) -> VehicleTypeModel:
        data = {"name": name}
        result = await VehicleTypeRepository.collection.insert_one(data)
        data["_id"] = result.inserted_id
        return VehicleTypeModel(data)

    @staticmethod
    async def get_all() -> list[VehicleTypeModel]:
        types = await VehicleTypeRepository.collection.find().to_list(100)
        return [VehicleTypeModel(t) for t in types]

    @staticmethod
    async def get_by_id(type_id: str) -> VehicleTypeModel | None:
        type_data = await VehicleTypeRepository.collection.find_one({"_id": ObjectId(type_id)})
        return VehicleTypeModel(type_data) if type_data else None

    @staticmethod
    async def update(type_id: str, name: str) -> VehicleTypeModel | None:
        result = await VehicleTypeRepository.collection.find_one_and_update(
            {"_id": ObjectId(type_id)},
            {"$set": {"name": name}},
            return_document=True
        )
        return VehicleTypeModel(result) if result else None

    @staticmethod
    async def delete_by_name(name: str) -> bool:
        result = await VehicleTypeRepository.collection.delete_one({"name": name})
        return result.deleted_count > 0