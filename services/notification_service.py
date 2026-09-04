from repositories.notification_repository import NotificationRepository
from repositories.user_repository import UserRepository


class NotificationService:
    """Service xử lý logic nghiệp vụ cho notifications"""
    
    @staticmethod
    async def create_notification(user_id: str, title: str, message: str, notif_type: str = "info"):
        """Tạo thông báo cho 1 user"""
        data = {
            "user_id": user_id,
            "title": title,
            "message": message,
            "type": notif_type,
        }
        return await NotificationRepository.create(data)
    
    @staticmethod
    async def create_notification_for_all_users(title: str, message: str, notif_type: str = "info"):
        """Tạo thông báo cho tất cả users"""
        users = await UserRepository.get_all()
        created = []
        for user in users:
            notif = await NotificationService.create_notification(
                user_id=str(user.id),
                title=title,
                message=message,
                notif_type=notif_type
            )
            created.append(notif)
        return created
    
    @staticmethod
    async def create_notification_for_admins(title: str, message: str, notif_type: str = "info"):
        """Tạo thông báo cho tất cả admins"""
        admins = await UserRepository.get_admins()
        created = []
        for admin in admins:
            notif = await NotificationService.create_notification(
                user_id=str(admin.id),
                title=title,
                message=message,
                notif_type=notif_type
            )
            created.append(notif)
        return created
    
    @staticmethod
    async def get_user_notifications(user_id: str, limit: int = 50):
        """Lấy danh sách thông báo của user"""
        return await NotificationRepository.get_by_user_id(user_id, limit)
    
    @staticmethod
    async def get_unread_count(user_id: str):
        """Đếm số thông báo chưa đọc"""
        return await NotificationRepository.get_unread_count(user_id)
    
    @staticmethod
    async def mark_as_read(notification_id: str):
        """Đánh dấu đã đọc"""
        return await NotificationRepository.mark_as_read(notification_id)
    
    @staticmethod
    async def mark_all_as_read(user_id: str):
        """Đánh dấu tất cả là đã đọc"""
        return await NotificationRepository.mark_all_as_read(user_id)
    
    @staticmethod
    async def delete_notification(notification_id: str):
        """Xóa thông báo"""
        return await NotificationRepository.delete_by_id(notification_id)
    
    @staticmethod
    async def delete_all_notifications(user_id: str):
        """Xóa tất cả thông báo của user"""
        return await NotificationRepository.delete_all_by_user(user_id)
    
    @staticmethod
    async def get_all_notifications(limit: int = 100):
        """Lấy tất cả notifications (admin - activity logs)"""
        return await NotificationRepository.get_all(limit)
