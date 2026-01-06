# routers/invoice_router.py
from fastapi import APIRouter
from controllers.invoice_controller import InvoiceController
from schemas.invoice_schema import InvoiceCreate, InvoiceResponse

router = APIRouter(prefix="/invoices", tags=["Invoices"])

# Khởi tạo controller (giả sử bạn inject service ở đây)
invoice_controller = InvoiceController(service=None)  # service thực tế cần inject


@router.post("/check-in", response_model=InvoiceResponse)
async def check_in(data: InvoiceCreate):
    """Check-in: tạo hóa đơn mới"""
    return await invoice_controller.check_in(data.dict())


@router.post("/check-out/{invoice_id}", response_model=InvoiceResponse)
async def check_out(invoice_id: str):
    """Check-out: cập nhật giờ ra, tính duration và tổng tiền"""
    return await invoice_controller.check_out(invoice_id)
