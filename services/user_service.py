import os
import pytz
import smtplib
import asyncio
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from repositories.user_repository import UserRepository
from repositories.invoice_repository import InvoiceRepository
from schemas.user_schema import UserSignup, UserSignin, UserUpdate

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
    async def check_in(user: UserSignin):
        existing = await UserRepository.find_by_phone(user.phone)
        if not existing or existing.password != user.password:
            raise ValueError("Invalid phone or password")

        start_time = UserService.now_gmt7()
        invoice_data = {
            "user_id": existing.id,
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
                f"Thời gian check-in: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                f"Cảm ơn bạn đã sử dụng dịch vụ!"
            )
            await UserService.send_email(
                to_email=existing.email, subject=subject, body=body
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

        update_data = {
            "end_time": end_time,
            "duration": total_seconds / 3600,
            "total_price": round(total_amount, 0),
            "status": "Deactive",
        }
        updated_invoice = await InvoiceRepository.updateInvoice(invoice.id, update_data)

        new_balance = existing.balance - total_amount
        if new_balance < 0:
            raise ValueError("Insufficient balance")
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
