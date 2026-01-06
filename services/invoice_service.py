from datetime import datetime


class InvoiceService:
    def __init__(self, invoice_repo, user_repo, plot_repo):
        self.invoice_repo = invoice_repo
        self.user_repo = user_repo
        self.plot_repo = plot_repo

    async def create_invoice(self, data):
        """Quy trình Xe vào (Check-in)"""
        # 1. Kiểm tra trạng thái bãi xe
        plot = self.plot_repo.getPLotById(data.parking_lot_id)
        if not plot or plot.status == "occupied":
            raise ValueError("Vị trí đỗ không khả dụng")

        # 2. Tạo bản ghi hóa đơn
        invoice_dict = {
            "user_id": data.user_id,
            "parking_lot_id": data.parking_lot_id,
            "start_time": datetime.utcnow(),
            "end_time": None,
            "duration": 0.0,
            "total_price": 0.0,
        }

        # 3. Cập nhật bãi xe sang 'occupied'
        self.plot_repo.updatePlot(data.parking_lot_id, {"status": "occupied"})
        return self.invoice_repo.createInvoice(invoice_dict)

    async def complete_invoice(self, invoice_id: str):
        """Quy trình Xe ra & Thanh toán (Check-out)"""
        # 1. Lấy thông tin hóa đơn & giá bãi xe
        invoice = self.invoice_repo.getInvoiceById(invoice_id)
        plot = self.plot_repo.getPLotById(invoice.parking_lot_id)
        user = self.user_repo.getUserById(invoice.user_id)

        # 2. Tính toán thời gian và tiền bạc
        end_time = datetime.utcnow()
        duration_delta = end_time - invoice.start_time
        duration_hours = max(duration_delta.total_seconds() / 3600, 0.1)
        total_price = round(duration_hours * plot.unit_price, 2)

        # 3. Kiểm tra số dư người dùng
        if user.balance < total_price:
            raise ValueError(
                f"Số dư không đủ. Cần {total_price}, hiện có {user.balance}"
            )

        # 4. THỰC HIỆN THANH TOÁN
        # - Trừ tiền User
        self.user_repo.updateBalance(user.id, round(user.balance - total_price, 2))
        # - Giải phóng bãi xe
        self.plot_repo.updatePlot(invoice.parking_lot_id, {"status": "available"})
        # - Cập nhật hóa đơn
        update_data = {
            "end_time": end_time,
            "duration": round(duration_hours, 2),
            "total_price": total_price,
        }
        return self.invoice_repo.updateInvoice(invoice_id, update_data)
