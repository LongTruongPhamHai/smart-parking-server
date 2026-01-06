from repositories.user_repository import UserRepository
from schemas.user_schema import UserSignup, UserSignin, UserUpdate
from repositories.invoice_repository import InvoiceRepository
from datetime import datetime, timedelta


class UserService:
    @staticmethod
    async def signup(user: UserSignup):
        """
        Tạo người dùng mới nếu số điện thoại chưa tồn tại
        """
        existing = await UserRepository.find_by_phone(user.phone)
        if existing:
            raise ValueError("Phone already exists")
        return await UserRepository.create(user.dict())

    @staticmethod
    async def signin(user: UserSignin):
        """
        Đăng nhập theo phone + password
        """
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
    async def update_user(user_id: str, user: UserUpdate):
        """
        Cập nhật thông tin user, bao gồm cả balance
        """
        return await UserRepository.update(user_id, user.dict(exclude_unset=True))

    @staticmethod
    async def add_balance(user_id: str, amount: float):
        """
        Nạp tiền vào tài khoản user
        - amount phải > 0
        - Trả về UserModel đã cập nhật balance
        """
        if amount <= 0:
            raise ValueError("Amount must be positive")

        updated_user = await UserRepository.add_balance(user_id, amount)
        if not updated_user:
            raise ValueError("User not found")
        return updated_user

    @staticmethod
    async def delete_user(user_id: str):
        return await UserRepository.delete(user_id)

    @staticmethod
    async def update_balance(user_id: str, amount: float):
        """
        Cập nhật số dư (nạp thêm hoặc trừ khi gửi xe)
        """
        user = await UserRepository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        new_balance = user.balance + amount
        return await UserRepository.update(user_id, {"balance": new_balance})

    @staticmethod
    async def check_in(user: UserSignin):
        """
        Khi người dùng vào bãi gửi xe:
        - Xác thực tài khoản
        - Tạo hóa đơn mới với giờ vào
        """
        existing = await UserRepository.find_by_phone(user.phone)
        if not existing or existing.password != user.password:
            raise ValueError("Invalid phone or password")

        invoice_data = {
            "user_id": existing.id,
            "start_time": datetime.utcnow(),
            "end_time": None,
            "total_amount": 0.0,
        }
        invoice = await InvoiceRepository.createInvoice(invoice_data)
        return invoice

    @staticmethod
    async def check_out(user: UserSignin):
        """
        Khi người dùng ra bãi gửi xe:
        - Xác thực tài khoản
        - Cập nhật hóa đơn gần nhất với end_time = giờ hiện tại
        - Tự tính duration, total_price, status trong updateInvoice
        - Trừ balance của user
        """
        existing = await UserRepository.find_by_phone(user.phone)
        if not existing or existing.password != user.password:
            raise ValueError("Invalid phone or password")

        invoices = await InvoiceRepository.getInvoiceByUserId(existing.id)
        if not invoices:
            raise ValueError("No invoice found for this user")

        invoice = max(invoices, key=lambda x: x.start_time)

        update_data = {"end_time": datetime.utcnow()}
        updated_invoice = await InvoiceRepository.updateInvoice(invoice.id, update_data)

        new_balance = existing.balance - updated_invoice.total_price
        if new_balance < 0:
            raise ValueError("Insufficient balance")
        await UserRepository.update(existing.id, {"balance": new_balance})

        return updated_invoice
