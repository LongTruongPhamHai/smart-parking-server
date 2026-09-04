from fastapi import HTTPException
from datetime import datetime
from schemas.invoice_schema import InvoiceResponse
from repositories.user_repository import UserRepository


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
            invoice = await self.service.complete_invoice(invoice_id)
            if not invoice:
                raise ValueError("Invoice not found or already completed")
            return InvoiceResponse(**invoice.to_dict())
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def get_all_invoices(self):
        """
        Lấy toàn bộ hóa đơn trong hệ thống
        """
        try:
            invoices = await self.service.get_all_invoices()
            result = []
            for inv in invoices:
                inv_dict = inv.to_dict()
                # Lookup user_name from user_id
                user = await UserRepository.get_by_id(inv_dict['user_id'])
                inv_dict['user_name'] = user.name if user else None
                result.append(InvoiceResponse(**inv_dict))
            return result
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def get_invoices_by_user_id(self, user_id: str):
        """
        Lấy danh sách hóa đơn của một user
        """
        try:
            invoices = await self.service.get_invoices_by_user_id(user_id)
            return [InvoiceResponse(**i.to_dict()) for i in invoices]
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
