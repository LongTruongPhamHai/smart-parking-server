class ParkingLotModel:
    def __init__(self, data: dict):
        self.id = str(data.get("_id")) if data.get("_id") else None
        self.name = data.get("name")
        self.unit_price = float(data.get("unit_price", 0.0))
        self.status = data.get("status", "available")  # Mặc định là trống

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "unit_price": self.unit_price,
            "status": self.status,
        }
