from bson import ObjectId


class ParkingTransactionModel:
    def __init__(self, data: dict):
        self.id = str(data.get("_id", "")) if data.get("_id") else None
        self.user_id = data.get("user_id")
        self.wallet_id = data.get("wallet_id")
        self.parking_lot_id = data.get("parking_lot_id")
        self.start_time = data.get("start_time")
        self.end_time = data.get("end_time")
        self.duration = data.get("duration")
        self.total_price = data.get("total_price")
        self.created_at = data.get("created_at")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "wallet_id": self.wallet_id,
            "parking_lot_id": self.parking_lot_id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration": self.duration,
            "total_price": self.total_price,
            "created_at": self.created_at,
        }
