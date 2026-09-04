from fastapi import APIRouter, Query
from controllers.notification_controller import NotificationController
from schemas.notification_schema import NotificationCreate, NotificationBroadcast

router = APIRouter(prefix="/api/notifications", tags=["Notifications"])


@router.get("/")
async def get_all_notifications(limit: int = Query(default=100, ge=1, le=500)):
    """Admin: Lấy tất cả notifications (activity logs)"""
    return await NotificationController.get_all_notifications(limit)


@router.post("/create")
async def create_notification(data: NotificationCreate):
    """Tạo notification cho 1 user cụ thể"""
    return await NotificationController.create_notification(data)


@router.post("/broadcast")
async def broadcast_notification(data: NotificationBroadcast):
    """Broadcast notification cho tất cả users hoặc admins"""
    return await NotificationController.broadcast_notification(data)


@router.get("/user/{user_id}")
async def get_user_notifications(user_id: str, limit: int = Query(default=50, ge=1, le=200)):
    """Lấy danh sách thông báo của user"""
    return await NotificationController.get_user_notifications(user_id, limit)


@router.put("/{notification_id}/read")
async def mark_as_read(notification_id: str):
    """Đánh dấu 1 thông báo là đã đọc"""
    return await NotificationController.mark_as_read(notification_id)


@router.put("/user/{user_id}/read-all")
async def mark_all_as_read(user_id: str):
    """Đánh dấu tất cả thông báo của user là đã đọc"""
    return await NotificationController.mark_all_as_read(user_id)


@router.delete("/{notification_id}")
async def delete_notification(notification_id: str):
    """Xóa 1 thông báo"""
    return await NotificationController.delete_notification(notification_id)


@router.delete("/user/{user_id}/all")
async def delete_all_notifications(user_id: str):
    """Xóa tất cả thông báo của user"""
    return await NotificationController.delete_all_notifications(user_id)
