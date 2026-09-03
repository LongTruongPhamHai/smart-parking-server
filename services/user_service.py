import os
import pytz
import smtplib
import asyncio
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from repositories.user_repository import UserRepository
from repositories.invoice_repository import InvoiceRepository
from repositories.parking_lot_repository import ParkingLotRepository
from schemas.user_schema import (
    UserSignup,
    UserSignin,
    UserUpdate,
    UserCreateAdmin,
    UserChangePassword,
    CheckInRequest,
)

# Load biến môi trường SMTP từ .env
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")


class UserService:
    tz = pytz.timezone("Asia/Bangkok")

    @staticmethod
    def now_gmt7():
        """Trả về thời gian hiện tại theo GMT+7"""
        return datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(UserService.tz)

    @staticmethod
    async def signup(user: UserSignup):
        """Tạo user mới nếu phone/email chưa tồn tại"""
        if await UserRepository.find_by_phone(user.phone):
            raise ValueError("Phone already exists")
        if user.email and await UserRepository.is_email_exists(user.email):
            raise ValueError("Email already exists")
        return await UserRepository.create(user.dict())

    @staticmethod
    async def admin_create_user(user: UserCreateAdmin):
        """Tạo user mới từ quyền Admin"""
        if await UserRepository.find_by_phone(user.phone):
            raise ValueError("Phone already exists")
        if user.email and await UserRepository.is_email_exists(user.email):
            raise ValueError("Email already exists")
        return await UserRepository.create(user.dict())

    @staticmethod
    async def signin(user: UserSignin):
        """Đăng nhập bằng phone + password"""
        existing = await UserRepository.find_by_phone(user.phone)
        if not existing or existing.password != user.password:
            raise ValueError("Invalid phone or password")
        return existing

    @staticmethod
    async def get_all_users():
        return await UserRepository.get_all()

    @staticmethod
    async def get_user_by_id(user_id: str):
        return await UserRepository.get_by_id(user_id)

    @staticmethod
    async def get_user_by_phone(phone: str):
        return await UserRepository.get_by_phone(phone)

    @staticmethod
    async def get_user_by_email(email: str):
        return await UserRepository.get_by_email(email)

    @staticmethod
    async def update_user(user_id: str, user: UserUpdate):
        return await UserRepository.update(user_id, user.dict(exclude_unset=True))

    @staticmethod
    async def change_password(user_id: str, pw_data: UserChangePassword):
        user = await UserRepository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        if user.password != pw_data.old_password:
            raise ValueError("Incorrect old password")
        return await UserRepository.update(user_id, {"password": pw_data.new_password})

    @staticmethod
    async def update_email(user_id: str, new_email: str):
        if await UserRepository.is_email_exists(new_email):
            raise ValueError("Email already exists")
        return await UserRepository.update_email(user_id, new_email)

    @staticmethod
    async def add_balance(user_id: str, amount: float):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        updated_user = await UserRepository.add_balance(user_id, amount)
        if not updated_user:
            raise ValueError("User not found")
        return updated_user

    @staticmethod
    async def update_balance(user_id: str, amount: float):
        user = await UserRepository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        new_balance = user.balance + amount
        return await UserRepository.update(user_id, {"balance": new_balance})

    @staticmethod
    async def delete_user(user_id: str):
        return await UserRepository.delete(user_id)

    @staticmethod
    async def check_in(user: CheckInRequest):
        existing = await UserRepository.find_by_phone(user.phone)
        if not existing or existing.password != user.password:
            raise ValueError("Invalid phone or password")

        # Find parking lot
        if user.parking_lot_id:
            assigned_lot = await ParkingLotRepository.getById(user.parking_lot_id)
            if not assigned_lot:
                raise ValueError("Parking lot not found")
            if assigned_lot.status != "available":
                raise ValueError("Selected parking lot is already occupied")
        else:
            all_lots = await ParkingLotRepository.getAll()
            available_lots = [lot for lot in all_lots if lot.status == "available"]
            if not available_lots:
                raise ValueError("Parking is full")
            assigned_lot = available_lots[0]

        # Mark lot as occupied
        await ParkingLotRepository.update(assigned_lot.id, {"status": "occupied"})

        start_time = UserService.now_gmt7()
        invoice_data = {
            "user_id": existing.id,
            "parking_lot_id": assigned_lot.id,
            "start_time": start_time,
            "end_time": None,
            "unit_price": 30000.0,
            "duration": 0.0,
            "total_price": 0.0,
            "status": "Active",
        }
        invoice = await InvoiceRepository.createInvoice(invoice_data)

        if existing.email:
            subject = "✅ Check-in thành công tại bãi xe"
            body = (
                f"Xin chào {existing.name},\n\n"
                f"Bạn vừa check-in tại bãi xe.\n"
                f"Vị trí đỗ: {assigned_lot.name}\n"
                f"Thời gian check-in: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                f"Cảm ơn bạn đã sử dụng dịch vụ!"
            )
            await UserService.send_email(
                to_email=existing.email, subject=subject, body=body
            )

        # Gửi mail thông báo cho Admin khi có xe vào bãi
        all_lots = await ParkingLotRepository.getAll()
        total_lots = len(all_lots)
        available_count = len([lot for lot in all_lots if lot.status == "available"])
        occupied_count = total_lots - available_count

        admins = await UserRepository.get_admins()
        for admin in admins:
            if admin.email:
                admin_subject = "🚗 Xe vào bãi — Cập nhật trạng thái bãi đỗ"
                admin_body = (
                    f"Xin chào Admin {admin.name},\n\n"
                    f"Có xe mới vào bãi đỗ.\n"
                    f"Khách hàng: {existing.name} ({existing.phone})\n"
                    f"Vị trí đỗ: {assigned_lot.name}\n"
                    f"Thời gian: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                    f"📊 Trạng thái bãi xe hiện tại:\n"
                    f"  • Tổng số chỗ: {total_lots}\n"
                    f"  • Đang sử dụng: {occupied_count}\n"
                    f"  • Còn trống: {available_count}\n\n"
                    f"Hệ thống Smart Parking thông báo tự động."
                )
                await UserService.send_email(
                    to_email=admin.email, subject=admin_subject, body=admin_body
                )

        return invoice

    @staticmethod
    async def check_out(user: UserSignin):
        existing = await UserRepository.find_by_phone(user.phone)
        if not existing or existing.password != user.password:
            raise ValueError("Invalid phone or password")

        invoices = await InvoiceRepository.getInvoiceByUserId(existing.id)
        if not invoices:
            raise ValueError("No invoice found for this user")

        invoice = max(invoices, key=lambda x: x.start_time)
        end_time = UserService.now_gmt7()

        if not invoice.start_time:
            raise ValueError("Invoice start_time is missing")

        start_time = invoice.start_time
        if start_time.tzinfo is None:
            start_time = start_time.replace(tzinfo=pytz.utc).astimezone(UserService.tz)

        total_seconds = max((end_time - start_time).total_seconds(), 60)
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)

        unit_price = invoice.unit_price or 30000.0

        if hours == 0:
            total_amount = unit_price
        else:
            hours_rounded = hours + (0.5 if minutes > 30 else 0)
            total_amount = unit_price * hours_rounded

        # Kiểm tra số dư TRƯỚC KHI thực hiện bất kỳ thay đổi nào
        new_balance = existing.balance - total_amount
        if new_balance < 0:
            raise ValueError("Insufficient balance")

        # Số dư đủ → cập nhật hóa đơn
        update_data = {
            "end_time": end_time,
            "duration": total_seconds / 3600,
            "total_price": round(total_amount, 0),
            "status": "Deactive",
        }
        updated_invoice = await InvoiceRepository.updateInvoice(invoice.id, update_data)

        # Giải phóng bãi đỗ
        if invoice.parking_lot_id:
            await ParkingLotRepository.update(
                invoice.parking_lot_id, {"status": "available"}
            )

        # Trừ tiền
        await UserRepository.update(existing.id, {"balance": new_balance})

        if existing.email:
            subject = "✅ Check-out thành công tại bãi xe"
            body = (
                f"Xin chào {existing.name},\n\n"
                f"Bạn vừa check-out tại bãi xe.\n"
                f"Thời gian check-in: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"Thời gian check-out: {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"Tổng tiền: {round(total_amount, 0):,.0f}₫\n"
                f"Số dư hiện tại: {new_balance:,.0f}₫\n\n"
                f"Cảm ơn bạn đã sử dụng dịch vụ!"
            )
            await UserService.send_email(
                to_email=existing.email, subject=subject, body=body
            )

        # Gửi mail thông báo cho Admin khi xe ra khỏi bãi
        all_lots = await ParkingLotRepository.getAll()
        total_lots = len(all_lots)
        available_count = len([lot for lot in all_lots if lot.status == "available"])
        occupied_count = total_lots - available_count

        admins = await UserRepository.get_admins()
        for admin in admins:
            if admin.email:
                admin_subject = "🚙 Xe ra khỏi bãi — Cập nhật trạng thái bãi đỗ"
                admin_body = (
                    f"Xin chào Admin {admin.name},\n\n"
                    f"Có xe vừa check-out rời khỏi bãi đỗ.\n"
                    f"Khách hàng: {existing.name} ({existing.phone})\n"
                    f"Thời gian check-in: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                    f"Thời gian check-out: {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                    f"Tổng tiền thanh toán: {round(total_amount, 0):,.0f}₫\n\n"
                    f"📊 Trạng thái bãi xe hiện tại:\n"
                    f"  • Tổng số chỗ: {total_lots}\n"
                    f"  • Đang sử dụng: {occupied_count}\n"
                    f"  • Còn trống: {available_count}\n\n"
                    f"Hệ thống Smart Parking thông báo tự động."
                )
                await UserService.send_email(
                    to_email=admin.email, subject=admin_subject, body=admin_body
                )

        return updated_invoice

    @staticmethod
    async def send_email(to_email: str, subject: str, body: str):
        """Gửi email async-safe qua SMTP"""
        msg = MIMEMultipart()
        msg["From"] = SMTP_USER
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, UserService._send_smtp, msg, to_email)

    @staticmethod
    def _send_smtp(msg: MIMEMultipart, to_email: str):
        """Gửi mail đồng bộ"""
        try:
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASS)
                server.send_message(msg)
        except Exception as e:
            print(f"Failed to send email to {to_email}: {e}")

    @staticmethod
    async def send_fire_alert():
        subject = "🔥 Cảnh báo cháy tại bãi xe!"
        now_gmt7 = datetime.utcnow() + timedelta(hours=7)
        now_str = now_gmt7.strftime("%Y-%m-%d %H:%M:%S")

        body = (
            f"Cảnh báo cháy được phát hiện!\nThời gian: {now_str}\n\n"
            "Vui lòng kiểm tra và hành động ngay!"
        )

        users = await UserRepository.get_all()
        for user in users:
            if user.email:
                await UserService.send_email(user.email, subject, body)

    @staticmethod
    async def send_gas_alert():
        subject = "⚠️ Cảnh báo khí GAS tại bãi xe!"
        now_gmt7 = datetime.utcnow() + timedelta(hours=7)
        now_str = now_gmt7.strftime("%Y-%m-%d %H:%M:%S")

        body = (
            f"Cảnh báo khí GAS được phát hiện!\nThời gian: {now_str}\n\n"
            "Vui lòng kiểm tra và hành động ngay!"
        )

        users = await UserRepository.get_all()
        for user in users:
            if user.email:
                await UserService.send_email(user.email, subject, body)
