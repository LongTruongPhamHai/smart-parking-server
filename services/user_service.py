from repositories.user_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user_schema import UserCreate, UserUpdate
from models.user_model import User

class UserService:

    @staticmethod
    async def signup(db: AsyncSession, user_data: UserCreate):
        user = User(
            name=user_data.name,
            email=user_data.email,
            phone=user_data.phone,
            password=user_data.password  
        )
        return await UserRepository.create(db, user)

    @staticmethod
    async def signin(db: AsyncSession, email: str, password: str):
        user = await UserRepository.get_by_email(db, email)
        if not user or user.password != password:
            return None
        return user

    @staticmethod
    async def get_users(db: AsyncSession):
        return await UserRepository.get_all(db)

    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int):
        return await UserRepository.get_by_id(db, user_id)

    @staticmethod
    async def update(db: AsyncSession, user_id: int, data: UserUpdate):
        user = await UserRepository.get_by_id(db, user_id)
        if not user:
            return None
        if data.name:
            user.name = data.name
        if data.email:
            user.email = data.email
        if data.phone:
            user.phone = data.phone
        if data.password:
            user.password = data.password  
        return await UserRepository.update(db, user)

    @staticmethod
    async def delete(db: AsyncSession, user_id: int):
        user = await UserRepository.get_by_id(db, user_id)
        if not user:
            return None
        return await UserRepository.delete(db, user)
