from fastapi import HTTPException
from schemas.invoice_schema import InvoiceResponse


class InvoiceController:
    def __init__(self, service):
        self.service = service

    async def check_in(self, data):
        try:
            invoice = await self.service.create_invoice(data)
            return InvoiceResponse(**invoice.to_dict())
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def check_out(self, invoice_id: str):
        try:
            invoice = await self.service.complete_invoice(invoice_id)
            return InvoiceResponse(**invoice.to_dict())
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
