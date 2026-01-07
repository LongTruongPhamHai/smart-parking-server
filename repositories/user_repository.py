from db import db
from models.user_model import UserModel
from datetime import datetime
from bson import ObjectId


class UserRepository:
    collection = db["users"]

    @staticmethod
    async def create(user_data: dict) -> UserModel:
        user_data["role"] = user_data.get("role", "Customer")
        user_data["balance"] = float(user_data.get("balance", 0.0))
        result = await UserRepository.collection.insert_one(user_data)
        user_data["_id"] = result.inserted_id
        return UserModel(user_data)

    @staticmethod
    async def find_by_phone(phone: str) -> UserModel | None:
        user = await UserRepository.collection.find_one({"phone": phone})
        return UserModel(user) if user else None

    @staticmethod
    async def get_all() -> list[UserModel]:
        users = await UserRepository.collection.find().to_list(100)
        return [UserModel(u) for u in users]

    @staticmethod
    async def get_by_id(user_id: str) -> UserModel | None:
        user = await UserRepository.collection.find_one({"_id": ObjectId(user_id)})
        return UserModel(user) if user else None

    @staticmethod
    async def get_by_phone(phone: str) -> UserModel | None:
        user = await UserRepository.collection.find_one({"phone": phone})
        return UserModel(user) if user else None

    @staticmethod
    async def update(user_id: str, update_data: dict) -> UserModel | None:
        if "balance" in update_data:
            update_data["balance"] = float(update_data["balance"])
        result = await UserRepository.collection.find_one_and_update(
            {"_id": ObjectId(user_id)}, {"$set": update_data}, return_document=True
        )
        return UserModel(result) if result else None

    @staticmethod
    async def add_balance(user_id: str, amount: float) -> UserModel | None:
        """
        Nạp tiền vào tài khoản user
        """
        if amount <= 0:
            raise ValueError("Amount must be positive")

        user = await UserRepository.get_by_id(user_id)
        if not user:
            return None

        new_balance = user.balance + amount
        update_data = {"balance": new_balance}
        result = await UserRepository.collection.find_one_and_update(
            {"_id": ObjectId(user_id)}, {"$set": update_data}, return_document=True
        )
        return UserModel(result) if result else None

    @staticmethod
    async def delete(user_id: str) -> bool:
        result = await UserRepository.collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0

    @staticmethod
    async def find_by_email(email: str) -> UserModel | None:
        """
        Tìm user theo email
        """
        user = await UserRepository.collection.find_one({"email": email})
        return UserModel(user) if user else None

    @staticmethod
    async def get_by_email(email: str) -> UserModel | None:
        """
        Lấy user theo email (tương tự find_by_email)
        """
        return await UserRepository.find_by_email(email)

    @staticmethod
    async def update_email(user_id: str, new_email: str) -> UserModel | None:
        """
        Cập nhật email của user
        """
        update_data = {"email": new_email}
        result = await UserRepository.collection.find_one_and_update(
            {"_id": ObjectId(user_id)}, {"$set": update_data}, return_document=True
        )
        return UserModel(result) if result else None

    @staticmethod
    async def is_email_exists(email: str) -> bool:
        """
        Kiểm tra email đã tồn tại chưa
        """
        user = await UserRepository.collection.find_one({"email": email})
        return user is not None
