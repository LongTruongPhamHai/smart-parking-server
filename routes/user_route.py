from fastapi import APIRouter
from db import db
from repositories.invoice_repository import InvoiceRepository
from repositories.user_repository import UserRepository
from repositories.parking_lot_repository import ParkingLotRepository
from services.invoice_service import InvoiceService
from controllers.invoice_controller import InvoiceController
from schemas.invoice_schema import InvoiceCreate, InvoiceResponse

router = APIRouter(prefix="/invoices", tags=["Invoices"])

# Khởi tạo DI
invoice_repo = InvoiceRepository(db["invoices"])
user_repo = UserRepository(db["users"])
plot_repo = ParkingLotRepository(db["parking_lots"])

service = InvoiceService(invoice_repo, user_repo, plot_repo)
controller = InvoiceController(service)


@router.post("/check-in", response_model=InvoiceResponse)
async def check_in(data: InvoiceCreate):
    return await controller.check_in(data)


@router.post("/check-out/{invoice_id}", response_model=InvoiceResponse)
async def check_out(invoice_id: str):
    return await controller.check_out(invoice_id)
