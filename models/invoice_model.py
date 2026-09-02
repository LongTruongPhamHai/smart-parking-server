from bson import ObjectId
from datetime import datetime


class InvoiceModel:
    def __init__(self, data: dict):
        self.id = str(data.get("_id", "")) if data.get("_id") else None
        self.user_id = data.get("user_id")
        self.parking_lot_id = data.get("parking_lot_id")
        self.start_time = data.get("start_time")
        self.end_time = data.get("end_time")
        self.unit_price = float(data.get("unit_price", 0.0))
        self.duration = float(data.get("duration", 0.0))
        self.total_price = float(data.get("total_price", 0.0))
        self.status = data.get("status", "Active")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "parking_lot_id": self.parking_lot_id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "unit_price": self.unit_price,
            "duration": self.duration,
            "total_price": self.total_price,
            "status": self.status,
        }
