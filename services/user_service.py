from repositories.user_repository import UserRepository
from schemas.user_schema import UserSignup, UserSignin, UserUpdate

class UserService:
    @staticmethod
    async def signup(user: UserSignup):
        existing = await UserRepository.find_by_phone(user.phone)
        if existing:
            raise ValueError("Phone already exists")
        return await UserRepository.create(user.dict())

    @staticmethod
    async def signin(user: UserSignin):
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
    async def delete_user(user_id: str):
        return await UserRepository.delete(user_id)