# routers/invoice_router.py
from fastapi import APIRouter
from controllers.invoice_controller import InvoiceController
from schemas.invoice_schema import InvoiceCreate, InvoiceResponse
from services.invoice_service import InvoiceService
from repositories.invoice_repository import InvoiceRepository
from repositories.user_repository import UserRepository
from repositories.parking_lot_repository import ParkingLotRepository


invoice_service = InvoiceService(
    invoice_repo=InvoiceRepository,
    user_repo=UserRepository,
    plot_repo=ParkingLotRepository,
)

invoice_controller = InvoiceController(service=invoice_service)

router = APIRouter(prefix="/invoices", tags=["Invoices"])


@router.post("/check-in", response_model=InvoiceResponse)
async def check_in(data: InvoiceCreate):
    """Xe vào bãi → tạo hóa đơn"""
    return await invoice_controller.check_in(data)


@router.post("/check-out/{invoice_id}", response_model=InvoiceResponse)
async def check_out(invoice_id: str):
    """Xe ra bãi → thanh toán"""
    return await invoice_controller.check_out(invoice_id)


@router.get("/", response_model=list[InvoiceResponse])
async def get_all_invoices():
    """Admin: xem toàn bộ hóa đơn"""
    return await invoice_controller.get_all_invoices()


@router.get("/user/{user_id}", response_model=list[InvoiceResponse])
async def get_invoices_by_user(user_id: str):
    """User/Admin: xem lịch sử gửi xe của user"""
    return await invoice_controller.get_invoices_by_user_id(user_id)
