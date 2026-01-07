from repositories.user_repository import UserRepository
from schemas.user_schema import UserSignup, UserSignin, UserUpdate
from repositories.invoice_repository import InvoiceRepository
from datetime import datetime, timedelta
import pytz


class UserService:
    tz = pytz.timezone("Asia/Bangkok")  # GMT+7

    @staticmethod
    def now_gmt7():
        """Trả về thời gian hiện tại theo GMT+7"""
        return datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(UserService.tz)

    # ======================
    # User signup / signin
    # ======================
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

    # ======================
    # Lấy thông tin user
    # ======================
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

    # ======================
    # Cập nhật user / balance / email
    # ======================
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

    # ======================
    # Check-in / Check-out
    # ======================
    @staticmethod
    async def check_in(user: UserSignin):
        existing = await UserRepository.find_by_phone(user.phone)
        if not existing or existing.password != user.password:
            raise ValueError("Invalid phone or password")

        invoice_data = {
            "user_id": existing.id,
            "start_time": UserService.now_gmt7(),
            "end_time": None,
            "total_amount": 0.0,
        }
        invoice = await InvoiceRepository.createInvoice(invoice_data)
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

        if invoice.start_time:
            if invoice.start_time.tzinfo is None:
                from datetime import timezone

                invoice_start = invoice.start_time.replace(
                    tzinfo=timezone.utc
                ).astimezone(UserService.tz)
            else:
                invoice_start = invoice.start_time

            duration_hours = max(
                (end_time - invoice_start).total_seconds() / 3600, 0.01
            )
        else:
            duration_hours = 0.0

        price_per_hour = 10.0
        total_amount = round(duration_hours * price_per_hour, 2)

        update_data = {
            "end_time": end_time,
            "duration": duration_hours,
            "total_amount": total_amount,
        }
        updated_invoice = await InvoiceRepository.updateInvoice(invoice.id, update_data)

        new_balance = existing.balance - total_amount
        if new_balance < 0:
            raise ValueError("Insufficient balance")
        await UserRepository.update(existing.id, {"balance": new_balance})

        return updated_invoice
