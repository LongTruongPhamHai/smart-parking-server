# repositories/parking_lot_repository.py
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId


class ParkingLotRepository:
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client.smart_parking_db
    collection = db["parking_lots"]

    @staticmethod
    async def add(data: dict):
        result = await ParkingLotRepository.collection.insert_one(data)
        return str(result.inserted_id)

    @staticmethod
    async def get_all():
        return await ParkingLotRepository.collection.find().to_list(length=None)

    @staticmethod
    async def get_by_id(plot_id: str):
        return await ParkingLotRepository.collection.find_one(
            {"_id": ObjectId(plot_id)}
        )

    @staticmethod
    async def update(plot_id: str, data: dict):
        await ParkingLotRepository.collection.update_one(
            {"_id": ObjectId(plot_id)}, {"$set": data}
        )

    @staticmethod
    async def delete(plot_id: str):
        await ParkingLotRepository.collection.delete_one({"_id": ObjectId(plot_id)})
