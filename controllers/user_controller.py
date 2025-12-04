from services.user_service import UserService
from schemas.user_schema import UserCreate, UserLogin, UserUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class UserController:

    @staticmethod
    async def signup(user_data: UserCreate, db: AsyncSession):
        return await UserService.signup(db, user_data)

    @staticmethod
    async def signin(login_data: UserLogin, db: AsyncSession):
        return await UserService.signin(db, login_data.email, login_data.password)

    @staticmethod
    async def get_users(db: AsyncSession):
        return await UserService.get_users(db)

    @staticmethod
    async def get_user_by_id(user_id: int, db: AsyncSession):
        return await UserService.get_user_by_id(db, user_id)

    @staticmethod
    async def update(user_id: int, data: UserUpdate, db: AsyncSession):
        return await UserService.update(db, user_id, data)

    @staticmethod
    async def delete(user_id: int, db: AsyncSession):
        return await UserService.delete(db, user_id)
