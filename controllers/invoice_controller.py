from fastapi import HTTPException
from datetime import datetime
from schemas.invoice_schema import InvoiceResponse


class InvoiceController:
    def __init__(self, service):
        self.service = service

    async def check_in(self, data: dict):
        """
        Check-in: tạo hóa đơn mới
        """
        try:
            invoice = await self.service.create_invoice(data)
            return InvoiceResponse(**invoice.to_dict())
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def check_out(self, invoice_id: str):
        """
        Check-out: cập nhật giờ ra, tính duration và tổng tiền
        """
        try:
            update_data = {"end_time": datetime.utcnow()}
            invoice = await self.service.complete_invoice(invoice_id, update_data)
            if not invoice:
                raise ValueError("Invoice not found or already completed")
            return InvoiceResponse(**invoice.to_dict())
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
