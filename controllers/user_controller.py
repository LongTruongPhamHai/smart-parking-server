from fastapi import HTTPException
from schemas.user_schema import UserResponse


class UserController:
    def __init__(self, service):
        self.service = service

    def signup(self, data):
        user = self.service.signUp(data)
        return UserResponse(**user.to_dict())

    def signin(self, credentials):
        user = self.service.signIn(credentials.phone, credentials.password)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return UserResponse(**user.to_dict())

    def get_users(self):
        users = self.service.getUsers()
        return [UserResponse(**u.to_dict()) for u in users]

    def get_user(self, user_id):
        user = self.service.getUserById(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse(**user.to_dict())

    def update_balance(self, user_id, balance):
        if not self.service.updateBalance(user_id, balance):
            raise HTTPException(status_code=404, detail="Update failed")
        return {"message": "Balance updated successfully"}
