from bson import ObjectId
from models.parking_lot_model import ParkingLotModel


class ParkingLotRepository:
    def __init__(self, db_collection):
        self.collection = db_collection

    def addPLot(self, plot_dict: dict):
        result = self.collection.insert_one(plot_dict)
        plot_dict["_id"] = result.inserted_id
        return ParkingLotModel(plot_dict)

    def getPLots(self):
        cursor = self.collection.find()
        return [ParkingLotModel(p) for p in cursor]

    def getPLotById(self, id: str):
        data = self.collection.find_one({"_id": ObjectId(id)})
        return ParkingLotModel(data) if data else None

    def updatePlot(self, id: str, update_data: dict):
        result = self.collection.update_one(
            {"_id": ObjectId(id)}, {"$set": update_data}
        )
        return result.modified_count > 0

    def deletePlot(self, id: str):
        result = self.collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0
