class WalletModel:
    def __init__(self, data: dict):
        self.id = str(data.get("_id", "")) if data.get("_id") else None
        self.user_id = data.get("user_id")
        self.name = data.get("name")
        self.balance = data.get("balance", 0.0)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "balance": self.balance,
        }