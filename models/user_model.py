class UserModel:
    def __init__(self, data: dict):
        self.id = str(data.get("_id")) if data.get("_id") else None
        self.name = data.get("name")
        self.phone = data.get("phone")
        self.password = data.get("password")
        self.role = data.get("role", "user")
        self.balance = float(data.get("balance", 0.0))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "role": self.role,
            "balance": self.balance,
        }
