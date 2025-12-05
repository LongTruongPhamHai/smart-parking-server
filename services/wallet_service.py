from repositories.wallet_repository import WalletRepository

class WalletService:
    @staticmethod
    async def add_wallet(user_id: str, name: str):
        existing = await WalletRepository.get_by_user_id(user_id)
        if existing:
            raise ValueError("Wallet already exists for this user")
        return await WalletRepository.create(user_id)

    @staticmethod
    async def get_balance(wallet_id: str):
        wallet = await WalletRepository.get_by_id(wallet_id)
        if not wallet:
            raise ValueError("Wallet not found")
        return wallet.balance
    
    @staticmethod
    async def get_wallet_by_user_id(user_id: str):
        return await WalletRepository.get_by_user_id(user_id)

    @staticmethod
    async def add_funds(wallet_id: str, amount: float):
        wallet = await WalletRepository.get_by_id(wallet_id)
        if not wallet:
            raise ValueError("Wallet not found")
        new_balance = wallet.balance + amount
        return await WalletRepository.update_balance(wallet_id, new_balance)

    @staticmethod
    async def pay(wallet_id: str, amount: float):
        wallet = await WalletRepository.get_by_id(wallet_id)
        if not wallet:
            raise ValueError("Wallet not found")
        if wallet.balance < amount:
            raise ValueError("Insufficient balance")
        new_balance = wallet.balance - amount
        return await WalletRepository.update_balance(wallet_id, new_balance)
    
    @staticmethod
    async def update_wallet(wallet_id: str, name: str):
        updated = await WalletRepository.update_name(wallet_id, name)
        if not updated:
            raise ValueError("Wallet not found")
        return updated
    
    @staticmethod
    async def delete_wallet(wallet_id: str):
        wallet = await WalletRepository.get_by_id(wallet_id)
        if not wallet:
            raise ValueError("Wallet not found")
        if wallet.balance != 0:
            raise ValueError("Cannot delete wallet with non-zero balance")
        deleted = await WalletRepository.delete(wallet_id)
        if not deleted:
            raise ValueError("Delete failed")
        return True