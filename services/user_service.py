from schemas.user_schema import UserSignup, UserUpdate


class UserService:
    def __init__(self, repository):
        self.repository = repository

    def signUp(self, data: UserSignup):
        user_dict = data.model_dump()
        user_dict["role"] = "user"
        user_dict["balance"] = 0.0
        return self.repository.signUp(user_dict)

    def signIn(self, phone: str, password: str):
        return self.repository.signIn(phone, password)

    def getUsers(self):
        return self.repository.getUsers()

    def getUserById(self, user_id: str):
        return self.repository.getUserById(user_id)

    def updateUser(self, user_id: str, info: UserUpdate):
        update_data = {k: v for k, v in info.model_dump().items() if v is not None}
        return self.repository.updateUser(user_id, update_data)

    def updateBalance(self, user_id: str, balance: float):
        return self.repository.updateBalance(user_id, balance)

    def deleteUser(self, user_id: str):
        return self.repository.deleteUser(user_id)
