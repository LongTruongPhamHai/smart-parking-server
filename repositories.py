# repositories/invoice_repository.py
from motor.motor_asyncio import AsyncIOMotorCollection


class InvoiceRepository:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def create(self, data: dict):
        result = await self.collection.insert_one(data)
        return str(result.inserted_id)

    async def get_by_id(self, invoice_id: str):
        return await self.collection.find_one({"_id": invoice_id})

    async def update(self, invoice_id: str, update_data: dict):
        await self.collection.update_one({"_id": invoice_id}, {"$set": update_data})
