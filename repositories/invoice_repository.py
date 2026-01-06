from bson import ObjectId
from models.invoice_model import InvoiceModel


class InvoiceRepository:
    def __init__(self, db_collection):
        self.collection = db_collection

    def createInvoice(self, data: dict):  #
        result = self.collection.insert_one(data)
        data["_id"] = result.inserted_id
        return InvoiceModel(data)

    def getInvoiceById(self, id: str):  #
        data = self.collection.find_one({"_id": ObjectId(id)})
        return InvoiceModel(data) if data else None

    def getInvoiceByUserId(self, uid: str):  #
        cursor = self.collection.find({"user_id": uid})
        return [InvoiceModel(i) for i in cursor]

    def updateInvoice(self, id: str, update_data: dict):
        self.collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
        return self.getInvoiceById(id)
