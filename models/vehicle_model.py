class VehicleModel:
    def __init__(self, data: dict):
        self.id = str(data.get("_id", "")) if data.get("_id") else None
        self.user_id = data.get("user_id")
        self.license_plate = data.get("license_plate")
        self.type_id = data.get("type_id")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "license_plate": self.license_plate,
            "type_id": self.type_id,
        }