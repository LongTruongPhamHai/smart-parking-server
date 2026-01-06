from bson import ObjectId
from models.user_model import UserModel


class UserRepository:
    def __init__(self, db_collection):
        self.collection = db_collection

    def signUp(self, user_dict: dict):
        result = self.collection.insert_one(user_dict)
        user_dict["_id"] = result.inserted_id
        return UserModel(user_dict)

    def signIn(self, phone: str, password: str):
        user_data = self.collection.find_one({"phone": phone, "password": password})
        return UserModel(user_data) if user_data else None

    def getUsers(self):
        cursor = self.collection.find()
        return [UserModel(u) for u in cursor]

    def getUserById(self, user_id: str):
        user_data = self.collection.find_one({"_id": ObjectId(user_id)})
        return UserModel(user_data) if user_data else None

    def updateUser(self, user_id: str, update_data: dict):
        result = self.collection.update_one(
            {"_id": ObjectId(user_id)}, {"$set": update_data}
        )
        return result.modified_count > 0

    def updateBalance(self, user_id: str, balance: float):
        result = self.collection.update_one(
            {"_id": ObjectId(user_id)}, {"$set": {"balance": balance}}
        )
        return result.modified_count > 0

    def deleteUser(self, user_id: str):
        result = self.collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0
