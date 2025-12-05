from db import db
from models.vehicle_model import VehicleModel
from bson import ObjectId

class VehicleRepository:
    collection = db["vehicles"]

    @staticmethod
    async def create(vehicle_data: dict) -> VehicleModel:
        result = await VehicleRepository.collection.insert_one(vehicle_data)
        vehicle_data["_id"] = result.inserted_id
        return VehicleModel(vehicle_data)

    @staticmethod
    async def get_all() -> list[VehicleModel]:
        vehicles = await VehicleRepository.collection.find().to_list(100)
        return [VehicleModel(v) for v in vehicles]

    @staticmethod
    async def get_by_id(vehicle_id: str) -> VehicleModel | None:
        vehicle = await VehicleRepository.collection.find_one({"_id": ObjectId(vehicle_id)})
        return VehicleModel(vehicle) if vehicle else None

    @staticmethod
    async def get_by_user_id(user_id: str) -> list[VehicleModel]:
        vehicles = await VehicleRepository.collection.find({"user_id": user_id}).to_list(100)
        return [VehicleModel(v) for v in vehicles]

    @staticmethod
    async def update(vehicle_id: str, update_data: dict) -> VehicleModel | None:
        result = await VehicleRepository.collection.find_one_and_update(
            {"_id": ObjectId(vehicle_id)},
            {"$set": update_data},
            return_document=True
        )
        return VehicleModel(result) if result else None

    @staticmethod
    async def delete(vehicle_id: str) -> bool:
        result = await VehicleRepository.collection.delete_one({"_id": ObjectId(vehicle_id)})
        return result.deleted_count > 0