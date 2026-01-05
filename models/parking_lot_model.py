from bson import ObjectId


class ParkingLotModel:
    def __init__(self, data: dict):
        self.id = str(data.get("_id", "")) if data.get("_id") else None
        self.name = data.get("name")
        self.unit_price = data.get("unit_price")
        self.created_at = data.get("created_at")
        self.updated_at = data.get("updated_at")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "unit_price": self.unit_price,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
