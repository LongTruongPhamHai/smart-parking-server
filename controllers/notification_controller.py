from fastapi import HTTPException
from services.notification_service import NotificationService
from schemas.notification_schema import NotificationCreate, NotificationBroadcast


class NotificationController:
    """Controller xử lý các request liên quan đến notifications"""
    
    @staticmethod
    async def create_notification(data: NotificationCreate):
        """Tạo notification cho 1 user cụ thể"""
        try:
            result = await NotificationService.create_notification(
                user_id=data.user_id,
                title=data.title,
                message=data.message,
                notif_type=data.type
            )
            return {"success": True, "data": result}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @staticmethod
    async def broadcast_notification(data: NotificationBroadcast):
        """Broadcast notification cho nhiều users"""
        try:
            if data.target == "admins":
                result = await NotificationService.create_notification_for_admins(
                    title=data.title,
                    message=data.message,
                    notif_type=data.type
                )
            else:  # all
                result = await NotificationService.create_notification_for_all_users(
                    title=data.title,
                    message=data.message,
                    notif_type=data.type
                )
            return {"success": True, "count": len(result)}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @staticmethod
    async def get_user_notifications(user_id: str, limit: int = 50):
        """Lấy danh sách thông báo của user"""
        try:
            notifications = await NotificationService.get_user_notifications(user_id, limit)
            unread_count = await NotificationService.get_unread_count(user_id)
            return {
                "success": True,
                "data": notifications,
                "unread_count": unread_count
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @staticmethod
    async def mark_as_read(notification_id: str):
        """Đánh dấu 1 thông báo đã đọc"""
        try:
            success = await NotificationService.mark_as_read(notification_id)
            if not success:
                raise HTTPException(status_code=404, detail="Notification not found")
            return {"success": True, "message": "Marked as read"}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @staticmethod
    async def mark_all_as_read(user_id: str):
        """Đánh dấu tất cả thông báo của user là đã đọc"""
        try:
            count = await NotificationService.mark_all_as_read(user_id)
            return {"success": True, "marked_count": count}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @staticmethod
    async def delete_notification(notification_id: str):
        """Xóa 1 thông báo"""
        try:
            success = await NotificationService.delete_notification(notification_id)
            if not success:
                raise HTTPException(status_code=404, detail="Notification not found")
            return {"success": True, "message": "Notification deleted"}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @staticmethod
    async def delete_all_notifications(user_id: str):
        """Xóa tất cả thông báo của user"""
        try:
            count = await NotificationService.delete_all_notifications(user_id)
            return {"success": True, "deleted_count": count}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @staticmethod
    async def get_all_notifications(limit: int = 100):
        """Lấy tất cả notifications (admin - activity logs)"""
        try:
            notifications = await NotificationService.get_all_notifications(limit)
            return {
                "success": True,
                "data": notifications
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
