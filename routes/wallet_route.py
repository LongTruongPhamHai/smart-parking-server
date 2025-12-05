from fastapi import APIRouter
from controllers.wallet_controller import WalletController
from schemas.wallet_schema import WalletCreate, WalletFund, WalletPayment, WalletResponse

router = APIRouter(prefix="/wallets", tags=["Wallets"])

@router.post("/", response_model=WalletResponse)
async def add_wallet(wallet: WalletCreate):
    return await WalletController.add_wallet(wallet)

@router.get("/{wallet_id}/balance")
async def get_balance(wallet_id: str):
    return await WalletController.get_balance(wallet_id)

@router.get("/by-user/{user_id}", response_model=WalletResponse)
async def get_wallet_by_user_id(user_id: str):
    return await WalletController.get_wallet_by_user_id(user_id)

@router.post("/{wallet_id}/funds", response_model=WalletResponse)
async def add_funds(wallet_id: str, fund: WalletFund):
    return await WalletController.add_funds(wallet_id, fund)

@router.post("/{wallet_id}/pay", response_model=WalletResponse)
async def pay(wallet_id: str, payment: WalletPayment):
    return await WalletController.pay(wallet_id, payment)

@router.put("/{wallet_id}/name", response_model=WalletResponse)
async def update_wallet(wallet_id: str, name: str):
    return await WalletController.update_wallet(wallet_id, name)

@router.delete("/{wallet_id}")
async def delete_wallet(wallet_id: str):
    return await WalletController.delete_wallet(wallet_id)