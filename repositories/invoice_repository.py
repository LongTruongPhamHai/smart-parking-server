from bson import ObjectId
from datetime import datetime
from models.invoice_model import InvoiceModel
from db import db


class InvoiceRepository:
    collection = db["invoices"]

    @staticmethod
    async def createInvoice(data: dict) -> InvoiceModel:
        """
        Tạo hóa đơn mới khi xe check-in
        """
        now = datetime.utcnow()
        data.setdefault("start_time", now)
        data.setdefault("end_time", None)
        data.setdefault("unit_price", 50000.0)
        data.setdefault("duration", 0.0)
        data.setdefault("total_price", 0.0)
        data.setdefault("status", "Active")

        result = await InvoiceRepository.collection.insert_one(data)
        data["_id"] = result.inserted_id
        return InvoiceModel(data)

    @staticmethod
    async def getAllInvoices(limit: int = 100) -> list[InvoiceModel]:
        """
        Lấy toàn bộ hóa đơn (dành cho Admin)
        """
        cursor = InvoiceRepository.collection.find().sort("start_time", -1)
        invoices = await cursor.to_list(length=limit)
        return [InvoiceModel(i) for i in invoices]

    @staticmethod
    async def getInvoiceById(id: str) -> InvoiceModel | None:
        """
        Lấy hóa đơn theo id
        """
        data = await InvoiceRepository.collection.find_one({"_id": ObjectId(id)})
        return InvoiceModel(data) if data else None

    @staticmethod
    async def getInvoiceByUserId(uid: str) -> list[InvoiceModel]:
        """
        Lấy tất cả hóa đơn của một user
        """
        cursor = InvoiceRepository.collection.find({"user_id": uid})
        invoices = await cursor.to_list(length=100)
        return [InvoiceModel(i) for i in invoices]

    @staticmethod
    async def getInvoiceByPlot(plot_id: str) -> list[InvoiceModel]:
        """
        Lấy tất cả hóa đơn theo ô đỗ (dành cho Admin)
        """
        cursor = InvoiceRepository.collection.find({"parking_lot_id": plot_id})
        invoices = await cursor.to_list(length=100)
        return [InvoiceModel(i) for i in invoices]

    @staticmethod
    async def updateInvoice(id: str, update_data: dict) -> InvoiceModel | None:
        """
        Cập nhật hóa đơn khi check-out
        - Chỉ update hóa đơn Active
        - Nếu có end_time, tính duration và total_price theo:
            - < 1 giờ: 50.000
            - >= 1 giờ: 50.000 * số giờ (làm tròn 30 phút)
        """
        invoice_data = await InvoiceRepository.collection.find_one(
            {"_id": ObjectId(id)}
        )

        if not invoice_data:
            return None

        if invoice_data.get("status") != "Active":
            return InvoiceModel(invoice_data)

        if "end_time" in update_data and update_data["end_time"]:
            start_time = invoice_data.get("start_time")
            unit_price = float(invoice_data.get("unit_price", 50000.0))

            if start_time:
                duration = (update_data["end_time"] - start_time).total_seconds() / 3600
                duration = round(duration, 2)
                update_data["duration"] = duration

                if duration < 1:
                    total_price = unit_price
                else:
                    hours_rounded = round(duration * 2) / 2
                    total_price = unit_price * hours_rounded

                update_data["total_price"] = round(total_price, 0)

            update_data["status"] = "Deactive"

        await InvoiceRepository.collection.update_one(
            {"_id": ObjectId(id)}, {"$set": update_data}
        )
        return await InvoiceRepository.getInvoiceById(id)
