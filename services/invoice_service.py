from datetime import datetime


def timedelta_to_hms(td):
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


class InvoiceService:
    def __init__(self, invoice_repo, user_repo, plot_repo):
        self.invoice_repo = invoice_repo
        self.user_repo = user_repo
        self.plot_repo = plot_repo

    async def create_invoice(self, data):
        """Quy trình Xe vào (Check-in)"""
        plot = self.plot_repo.getPLotById(data.parking_lot_id)
        if not plot or plot.status == "occupied":
            raise ValueError("Vị trí đỗ không khả dụng")

        invoice_dict = {
            "user_id": data.user_id,
            "parking_lot_id": data.parking_lot_id,
            "start_time": datetime.utcnow(),
            "end_time": None,
            "duration": 0.0,
            "total_price": 0.0,
        }

        self.plot_repo.updatePlot(data.parking_lot_id, {"status": "occupied"})
        return self.invoice_repo.createInvoice(invoice_dict)

    async def complete_invoice(self, invoice_id: str):
        """Quy trình Xe ra & Thanh toán (Check-out)"""

        invoice = self.invoice_repo.getInvoiceById(invoice_id)
        plot = self.plot_repo.getPLotById(invoice.parking_lot_id)
        user = self.user_repo.getUserById(invoice.user_id)

        end_time = datetime.utcnow()
        duration_delta = end_time - invoice.start_time

        duration_hms = timedelta_to_hms(duration_delta)

        duration_hours = max(duration_delta.total_seconds() / 3600, 0.1)
        total_price = round(duration_hours * plot.unit_price, 2)

        if user.balance < total_price:
            raise ValueError(
                f"Số dư không đủ. Cần {total_price}, hiện có {user.balance}"
            )

        self.user_repo.updateBalance(user.id, round(user.balance - total_price, 2))
        self.plot_repo.updatePlot(invoice.parking_lot_id, {"status": "available"})

        update_data = {
            "end_time": end_time,
            "duration": duration_hms,
            "total_price": total_price,
            "status": "Deactive",
        }

        return self.invoice_repo.updateInvoice(invoice_id, update_data)

    async def get_all_invoices(self):
        """
        Lấy toàn bộ hóa đơn trong hệ thống (Admin)
        """
        invoices = await self.invoice_repo.getAllInvoices()
        return invoices

    async def get_invoices_by_user_id(self, user_id: str):
        """
        Lấy danh sách hóa đơn của 1 user
        """
        user = self.user_repo.getUserById(user_id)
        if not user:
            raise ValueError("User không tồn tại")

        invoices = self.invoice_repo.getInvoiceByUserId(user_id)
        return invoices
