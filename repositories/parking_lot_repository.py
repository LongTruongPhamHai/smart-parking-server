from bson import ObjectId
from models.parking_lot_model import ParkingLotModel
from db import db


class ParkingLotRepository:
    collection = db["parking_lots"]

    @staticmethod
    async def create(data: dict) -> ParkingLotModel:
        result = await ParkingLotRepository.collection.insert_one(data)
        data["_id"] = result.inserted_id
        return ParkingLotModel(data)

    @staticmethod
    async def getAll() -> list[ParkingLotModel]:
        cursor = ParkingLotRepository.collection.find()
        lots = await cursor.to_list(length=None)
        return [ParkingLotModel(lot) for lot in lots]

    @staticmethod
    async def getById(plot_id: str) -> ParkingLotModel | None:
        data = await ParkingLotRepository.collection.find_one(
            {"_id": ObjectId(plot_id)}
        )
        return ParkingLotModel(data) if data else None

    @staticmethod
    async def update(plot_id: str, data: dict) -> ParkingLotModel | None:
        await ParkingLotRepository.collection.update_one(
            {"_id": ObjectId(plot_id)},
            {"$set": data},
        )
        return await ParkingLotRepository.getById(plot_id)

    @staticmethod
    async def delete(plot_id: str) -> bool:
        result = await ParkingLotRepository.collection.delete_one(
            {"_id": ObjectId(plot_id)}
        )
        return result.deleted_count == 1
