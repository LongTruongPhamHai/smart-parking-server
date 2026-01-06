from fastapi import APIRouter
from controllers.invoice_controller import InvoiceController
from schemas.invoice_schema import InvoiceCreate, InvoiceResponse

router = APIRouter(prefix="/invoices", tags=["Invoices"])


@router.post("/", response_model=InvoiceResponse)
async def create_invoice(data: InvoiceCreate):
    """Tương ứng createInvoice(info) - Xe vào bãi"""
    return await InvoiceController.create_invoice(data)


@router.get("/", response_model=list[InvoiceResponse])
async def get_all_invoices():
    """Tương ứng getAllInvoices()"""
    return await InvoiceController.get_all_invoices()


@router.get("/{invoice_id}", response_model=InvoiceResponse)
async def get_invoice_by_id(invoice_id: str):
    """Tương ứng getInvoiceById(id)"""
    return await InvoiceController.get_invoice_by_id(invoice_id)


@router.get("/user/{user_id}", response_model=list[InvoiceResponse])
async def get_invoice_by_user_id(user_id: str):
    """Tương ứng getInvoiceByUserId(uid)"""
    return await InvoiceController.get_user_invoices(user_id)


@router.get("/plot/{plot_id}", response_model=list[InvoiceResponse])
async def get_invoice_by_plot(plot_id: str):
    """Tương ứng getInvoiceByPLot(plotid)"""
    return await InvoiceController.get_invoice_by_plot(plot_id)


@router.post("/checkout/{invoice_id}", response_model=InvoiceResponse)
async def complete_parking(invoice_id: str):
    """Kết thúc gửi xe, tính tiền và trừ balance của User"""
    return await InvoiceController.complete_parking(invoice_id)
