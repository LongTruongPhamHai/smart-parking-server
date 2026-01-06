from bson import ObjectId


class UserModel:
    def __init__(self, data: dict):
        self.id = str(data.get("_id", "")) if data.get("_id") else None
        self.name = data.get("name")
        self.phone = data.get("phone")
        self.password = data.get("password")
        self.role = data.get("role")
        self.balance = float(data.get("balance", 0.0))
        self.created_at = data.get("created_at")
        self.updated_at = data.get("updated_at")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "password": self.password,
            "role": self.role,
            "balance": self.balance,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
