from fastapi import HTTPException
from services.wallet_service import WalletService
from schemas.wallet_schema import WalletCreate, WalletFund, WalletPayment, WalletResponse

class WalletController:
    @staticmethod
    async def add_wallet(wallet: WalletCreate) -> WalletResponse:
        try:
            new_wallet = await WalletService.add_wallet(wallet.user_id, wallet.name)
            return WalletResponse(**new_wallet.to_dict())
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def get_balance(wallet_id: str) -> dict:
        try:
            balance = await WalletService.get_balance(wallet_id)
            return {"balance": balance}
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    @staticmethod
    async def get_wallet_by_user_id(user_id: str) -> WalletResponse:
        wallet = await WalletService.get_wallet_by_user_id(user_id)
        if not wallet:
            raise HTTPException(status_code=404, detail="Wallet not found for this user")
        return WalletResponse(**wallet.to_dict())

    @staticmethod
    async def add_funds(wallet_id: str, fund: WalletFund) -> WalletResponse:
        try:
            updated = await WalletService.add_funds(wallet_id, fund.amount)
            return WalletResponse(**updated.to_dict())
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def pay(wallet_id: str, payment: WalletPayment) -> WalletResponse:
        try:
            updated = await WalletService.pay(wallet_id, payment.amount)
            return WalletResponse(**updated.to_dict())
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        
    @staticmethod
    async def update_wallet(wallet_id: str, name: str) -> WalletResponse:
        try:
            updated = await WalletService.update_wallet(wallet_id, name)
            return WalletResponse(**updated.to_dict())
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        
    @staticmethod
    async def delete_wallet(wallet_id: str) -> dict:
        try:
            await WalletService.delete_wallet(wallet_id)
            return {"message": "Wallet deleted successfully"}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))