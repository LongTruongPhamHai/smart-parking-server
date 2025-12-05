from db import db
from models.wallet_model import WalletModel
from bson import ObjectId

class WalletRepository:
    collection = db["wallets"]

    @staticmethod
    async def create(user_id: str, name: str) -> WalletModel:
        wallet_data = {
            "user_id": user_id,
            "name": name,
            "balance": 0.0
        }
        result = await WalletRepository.collection.insert_one(wallet_data)
        wallet_data["_id"] = result.inserted_id
        return WalletModel(wallet_data)

    @staticmethod
    async def get_by_id(wallet_id: str) -> WalletModel | None:
        wallet = await WalletRepository.collection.find_one({"_id": ObjectId(wallet_id)})
        return WalletModel(wallet) if wallet else None

    @staticmethod
    async def get_by_user_id(user_id: str) -> WalletModel | None:
        wallet = await WalletRepository.collection.find_one({"user_id": user_id})
        return WalletModel(wallet) if wallet else None

    @staticmethod
    async def update_balance(wallet_id: str, new_balance: float) -> WalletModel | None:
        result = await WalletRepository.collection.find_one_and_update(
            {"_id": ObjectId(wallet_id)},
            {"$set": {"balance": new_balance}},
            return_document=True
        )
        return WalletModel(result) if result else None
    
    @staticmethod
    async def update_name(wallet_id: str, name: str) -> WalletModel | None:
        from bson import ObjectId
        result = await WalletRepository.collection.find_one_and_update(
            {"_id": ObjectId(wallet_id)},
            {"$set": {"name": name}},
            return_document=True
        )
        return WalletModel(result) if result else None

    @staticmethod
    async def delete(wallet_id: str) -> bool:
        from bson import ObjectId
        result = await WalletRepository.collection.delete_one({"_id": ObjectId(wallet_id)})
        return result.deleted_count > 0