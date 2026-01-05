from repositories.parking_transaction_repository import ParkingTransactionRepository
from repositories.parking_lot_repository import ParkingLotRepository
from datetime import datetime


class ParkingTransactionService:
    @staticmethod
    async def create_transaction(data: dict):
        """
        Logic khi xe vào bãi: Ghi nhận user_id, parking_lot_id và start_time
        """
        parking_lot = await ParkingLotRepository.getPLotById(data.get("parking_lot_id"))
        if not parking_lot:
            raise ValueError("Parking lot does not exist")

        data["price_id"] = str(parking_lot.unit_price)
        data["start_time"] = datetime.utcnow()

        return await ParkingTransactionRepository.createTransaction(data)

    @staticmethod
    async def get_transaction_by_id(transaction_id: str):
        transaction = await ParkingTransactionRepository.getTransactionById(
            transaction_id
        )
        if not transaction:
            raise ValueError("Transaction not found")
        return transaction

    @staticmethod
    async def get_all_transactions():
        return await ParkingTransactionRepository.getAllTransaction()

    @staticmethod
    async def get_user_history(user_id: str):
        return await ParkingTransactionRepository.get_by_user_id(user_id)

    @staticmethod
    async def complete_transaction(transaction_id: str):
        """
        Logic khi xe ra bãi: Tính duration và total_price
        """
        transaction = await ParkingTransactionRepository.getTransactionById(
            transaction_id
        )
        if not transaction:
            raise ValueError("Transaction not found")

        end_time = datetime.utcnow()
        duration_delta = end_time - transaction.start_time
        duration_hours = duration_delta.total_seconds() / 3600

        unit_price = float(transaction.price_id)
        total_price = duration_hours * unit_price

        update_data = {
            "end_time": end_time,
            "duration": round(duration_hours, 2),
            "total_price": round(total_price, 2),
        }

        return await ParkingTransactionRepository.collection.find_one_and_update(
            {"_id": transaction.id}, {"$set": update_data}, return_document=True
        )
