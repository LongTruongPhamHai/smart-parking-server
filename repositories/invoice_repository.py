from bson import ObjectId
from datetime import datetime
from models.invoice_model import InvoiceModel
from db import db
import pytz


class InvoiceRepository:
    collection = db["invoices"]
    tz = pytz.timezone("Asia/Bangkok")

    @staticmethod
    async def createInvoice(data: dict) -> InvoiceModel:
        """
        Tạo hóa đơn mới khi xe check-in
        """
        now_utc7 = (
            datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(InvoiceRepository.tz)
        )
        data.setdefault("start_time", now_utc7)
        data.setdefault("end_time", None)
        data.setdefault("unit_price", 30000.0)
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
        - Nếu có end_time, tính duration và total_price
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
            unit_price = float(invoice_data.get("unit_price", 30000.0))
            end_time = update_data["end_time"]

            if end_time.tzinfo is None:
                end_time = end_time.replace(tzinfo=pytz.utc).astimezone(
                    InvoiceRepository.tz
                )

            if start_time:
                if start_time.tzinfo is None:
                    start_time = start_time.replace(tzinfo=pytz.utc).astimezone(
                        InvoiceRepository.tz
                    )

                duration_hours = (end_time - start_time).total_seconds() / 3600
                duration_hours = max(duration_hours, 0.01)
                duration_hours = round(duration_hours, 2)
                update_data["duration"] = duration_hours

                if duration_hours < 1:
                    total_price = unit_price
                else:
                    hours_rounded = round(duration_hours * 2) / 2
                    total_price = unit_price * hours_rounded

                update_data["total_price"] = round(total_price, 0)

            update_data["end_time"] = end_time
            update_data["status"] = "Deactive"

        await InvoiceRepository.collection.update_one(
            {"_id": ObjectId(id)}, {"$set": update_data}
        )
        return await InvoiceRepository.getInvoiceById(id)
