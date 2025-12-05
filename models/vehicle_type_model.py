class VehicleTypeModel:
    def __init__(self, data: dict):
        self.id = str(data.get("_id", "")) if data.get("_id") else None
        self.name = data.get("name")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }