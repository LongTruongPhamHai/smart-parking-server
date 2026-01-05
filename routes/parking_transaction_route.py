from fastapi import APIRouter
from controllers.parking_transaction_controller import ParkingTransactionController
from schemas.parking_transaction_schema import TransactionCreate, TransactionResponse

router = APIRouter(prefix="/transactions", tags=["Parking Transactions"])


@router.post("/check-in", response_model=TransactionResponse)
async def create_transaction(data: TransactionCreate):
    """Bắt đầu gửi xe (Xe vào bãi)"""
    return await ParkingTransactionController.create_transaction(data)


@router.get("/", response_model=list[TransactionResponse])
async def get_all_transactions():
    return await ParkingTransactionController.get_all_transactions()


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction_by_id(transaction_id: str):
    return await ParkingTransactionController.get_transaction_by_id(transaction_id)


@router.get("/user/{user_id}", response_model=list[TransactionResponse])
async def get_user_transactions(user_id: str):
    """Lấy lịch sử giao dịch của một người dùng"""
    return await ParkingTransactionController.get_user_transactions(user_id)


@router.post("/check-out/{transaction_id}", response_model=TransactionResponse)
async def complete_parking(transaction_id: str):
    """Kết thúc gửi xe và tính tiền (Xe ra bãi)"""
    return await ParkingTransactionController.complete_parking(transaction_id)
