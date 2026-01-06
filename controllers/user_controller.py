from fastapi import HTTPException
from services.user_service import UserService
from schemas.user_schema import UserSignup, UserSignin, UserUpdate, UserResponse


class UserController:
    @staticmethod
    async def signup(user: UserSignup) -> UserResponse:
        try:
            new_user = await UserService.signup(user)
            return UserResponse(**new_user.to_dict())
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def signin(user: UserSignin) -> UserResponse:
        try:
            existing = await UserService.signin(user)
            return UserResponse(**existing.to_dict())
        except ValueError as e:
            raise HTTPException(status_code=401, detail=str(e))

    @staticmethod
    async def get_all_users() -> list[UserResponse]:
        users = await UserService.get_all_users()
        return [UserResponse(**u.to_dict()) for u in users]

    @staticmethod
    async def get_user_by_id(user_id: str) -> UserResponse:
        user = await UserService.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse(**user.to_dict())

    @staticmethod
    async def get_user_by_phone(phone: str) -> UserResponse:
        user = await UserService.get_user_by_phone(phone)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse(**user.to_dict())

    # Bỏ get_user_by_email vì không còn email

    @staticmethod
    async def update_user(user_id: str, user: UserUpdate) -> UserResponse:
        updated = await UserService.update_user(user_id, user)
        if not updated:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse(**updated.to_dict())

    # ==========================
    # Nạp tiền vào tài khoản
    # ==========================
    @staticmethod
    async def add_balance(user_id: str, amount: float) -> UserResponse:
        """
        Nạp tiền vào tài khoản người dùng
        """
        try:
            updated_user = await UserService.add_balance(user_id, amount)
            return UserResponse(**updated_user.to_dict())
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def delete_user(user_id: str) -> dict:
        deleted = await UserService.delete_user(user_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully"}

    # ==========================
    # Check in / Check out
    # ==========================
    @staticmethod
    async def check_in(user: UserSignin):
        try:
            invoice = await UserService.check_in(user)
            return {"message": "Check-in successful", "invoice_id": str(invoice.id)}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def check_out(user: UserSignin):
        try:
            invoice = await UserService.check_out(user)
            return {
                "message": "Check-out successful",
                "invoice_id": str(invoice.id),
                "total_amount": invoice.total_price,
            }
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
