class InvoiceModel:
    def __init__(self, data: dict):
        self.id = str(data.get("_id")) if data.get("_id") else None
        self.user_id = data.get("user_id")  #
        self.parking_lot_id = data.get("parking_lot_id")  #
        self.start_time = data.get("start_time")  #
        self.end_time = data.get("end_time")  #
        self.duration = float(data.get("duration", 0.0))  #
        self.total_price = float(data.get("total_price", 0.0))  #

    def to_dict(self):
        return self.__dict__
