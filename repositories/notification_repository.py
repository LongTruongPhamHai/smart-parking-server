from bson import ObjectId
from datetime import datetime
from db import db
from repositories.user_repository import UserRepository


class NotificationRepository:
    """Repository để thao tác với collection notifications"""
    
    collection = db["notifications"]
    
    @staticmethod
    async def create(data: dict):
        """Tạo notification mới"""
        data["created_at"] = datetime.utcnow()
        data["is_read"] = False
        result = await NotificationRepository.collection.insert_one(data)
        data["_id"] = str(result.inserted_id)
        return data
    
    @staticmethod
    async def get_by_user_id(user_id: str, limit: int = 50):
        """Lấy tất cả thông báo của user, sắp xếp mới nhất trước"""
        cursor = NotificationRepository.collection.find(
            {"user_id": user_id}
        ).sort("created_at", -1).limit(limit)
        
        notifications = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            notifications.append(doc)
        return notifications
    
    @staticmethod
    async def get_unread_count(user_id: str):
        """Đếm số thông báo chưa đọc của user"""
        count = await NotificationRepository.collection.count_documents(
            {"user_id": user_id, "is_read": False}
        )
        return count
    
    @staticmethod
    async def mark_as_read(notification_id: str):
        """Đánh dấu 1 thông báo là đã đọc"""
        result = await NotificationRepository.collection.update_one(
            {"_id": ObjectId(notification_id)},
            {"$set": {"is_read": True}}
        )
        return result.modified_count > 0
    
    @staticmethod
    async def mark_all_as_read(user_id: str):
        """Đánh dấu tất cả thông báo của user là đã đọc"""
        result = await NotificationRepository.collection.update_many(
            {"user_id": user_id, "is_read": False},
            {"$set": {"is_read": True}}
        )
        return result.modified_count
    
    @staticmethod
    async def delete_by_id(notification_id: str):
        """Xóa 1 thông báo"""
        result = await NotificationRepository.collection.delete_one(
            {"_id": ObjectId(notification_id)}
        )
        return result.deleted_count > 0
    
    @staticmethod
    async def delete_all_by_user(user_id: str):
        """Xóa tất cả thông báo của user"""
        result = await NotificationRepository.collection.delete_many(
            {"user_id": user_id}
        )
        return result.deleted_count
    
    @staticmethod
    async def get_all(limit: int = 100):
        """Lấy tất cả notifications dành cho admin users, sắp xếp mới nhất trước (admin - activity logs)"""
        # Get all admin user IDs
        admin_users = await UserRepository.get_admins()
        admin_ids = [str(admin.id) for admin in admin_users]
        
        # Query notifications where user_id is one of admin IDs
        cursor = NotificationRepository.collection.find(
            {"user_id": {"$in": admin_ids}}
        ).sort("created_at", -1).limit(limit)
        
        notifications = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            notifications.append(doc)
        return notifications
