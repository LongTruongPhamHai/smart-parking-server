from db import db
from datetime import datetime
from bson import ObjectId
from models.parking_lot_model import ParkingLotModel


class ParkingLotRepository:
    collection = db["parking_lots"]

    @staticmethod
    async def addPLot(plot_data: dict) -> ParkingLotModel:
        """
        plot_data: { "name": str, "unit_price": float }
        """
        plot_data["created_at"] = datetime.utcnow()
        plot_data["updated_at"] = datetime.utcnow()
        result = await ParkingLotRepository.collection.insert_one(plot_data)
        plot_data["_id"] = result.inserted_id
        return ParkingLotModel(plot_data)

    @staticmethod
    async def getPLots() -> list[ParkingLotModel]:
        plots = await ParkingLotRepository.collection.find().to_list(length=100)
        return [ParkingLotModel(p) for p in plots]

    @staticmethod
    async def getPLotById(id: str) -> ParkingLotModel | None:
        plot = await ParkingLotRepository.collection.find_one({"_id": ObjectId(id)})
        return ParkingLotModel(plot) if plot else None

    @staticmethod
    async def updatePlot(id: str, update_data: dict) -> ParkingLotModel | None:
        update_data["updated_at"] = datetime.utcnow()
        result = await ParkingLotRepository.collection.find_one_and_update(
            {"_id": ObjectId(id)}, {"$set": update_data}, return_document=True
        )
        return ParkingLotModel(result) if result else None

    @staticmethod
    async def deletePlot(id: str) -> bool:
        result = await ParkingLotRepository.collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0
