from fastapi import HTTPException
from services.parking_transaction_service import ParkingTransactionService
from schemas.parking_transaction_schema import TransactionCreate, TransactionResponse


class ParkingTransactionController:
    @staticmethod
    async def create_transaction(data: TransactionCreate) -> TransactionResponse:
        try:
            # Xử lý logic lúc xe vào bãi
            new_transaction = await ParkingTransactionService.create_transaction(
                data.dict()
            )
            return TransactionResponse(**new_transaction.to_dict())
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def get_transaction_by_id(transaction_id: str) -> TransactionResponse:
        try:
            transaction = await ParkingTransactionService.get_transaction_by_id(
                transaction_id
            )
            return TransactionResponse(**transaction.to_dict())
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    @staticmethod
    async def get_all_transactions() -> list[TransactionResponse]:
        transactions = await ParkingTransactionService.get_all_transactions()
        return [TransactionResponse(**t.to_dict()) for t in transactions]

    @staticmethod
    async def get_user_transactions(user_id: str) -> list[TransactionResponse]:
        transactions = await ParkingTransactionService.get_user_history(user_id)
        return [TransactionResponse(**t.to_dict()) for t in transactions]

    @staticmethod
    async def complete_parking(transaction_id: str) -> TransactionResponse:
        """Endpoint gọi khi xe ra khỏi bãi để tính tiền"""
        try:
            completed = await ParkingTransactionService.complete_transaction(
                transaction_id
            )
            if not completed:
                raise HTTPException(status_code=404, detail="Transaction not found")
            return TransactionResponse(**completed.to_dict())
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
