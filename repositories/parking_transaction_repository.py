from db import db
from datetime import datetime
from bson import ObjectId
from models.parking_transaction_model import ParkingTransactionModel


class ParkingTransactionRepository:
    collection = db["parking_transactions"]

    @staticmethod
    async def createTransaction(transaction_data: dict) -> ParkingTransactionModel:
        """
        transaction_data: {
            "user_id": str, "wallet_id": str, "parking_lot_id": str,
            "start_time": time, "end_time": time, "price_id": str,
            "duration": float, "total_price": float
        }
        """
        transaction_data["created_at"] = datetime.utcnow()
        result = await ParkingTransactionRepository.collection.insert_one(
            transaction_data
        )
        transaction_data["_id"] = result.inserted_id
        return ParkingTransactionModel(transaction_data)

    @staticmethod
    async def getTransactionById(ptid: str) -> ParkingTransactionModel | None:
        transaction = await ParkingTransactionRepository.collection.find_one(
            {"_id": ObjectId(ptid)}
        )
        return ParkingTransactionModel(transaction) if transaction else None

    @staticmethod
    async def getAllTransaction() -> list[ParkingTransactionModel]:
        transactions = await ParkingTransactionRepository.collection.find().to_list(
            length=1000
        )
        return [ParkingTransactionModel(t) for t in transactions]

    @staticmethod
    async def get_by_user_id(user_id: str) -> list[ParkingTransactionModel]:
        transactions = await ParkingTransactionRepository.collection.find(
            {"user_id": user_id}
        ).to_list(length=100)
        return [ParkingTransactionModel(t) for t in transactions]
