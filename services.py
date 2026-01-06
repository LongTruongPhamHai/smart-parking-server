import math
from datetime import datetime


class ParkingService:
    def __init__(self, user_repo, plot_repo, invoice_repo):
        self.user_repo = user_repo
        self.plot_repo = plot_repo
        self.invoice_repo = invoice_repo

    async def checkIn(self, phone, password, plot_id, unit_price):
        # 1. User đăng nhập để check-in
        user = self.user_repo.signIn(phone, password)
        if not user:
            raise ValueError("Sai thông tin tài khoản!")

        # 2. Tạo hóa đơn (createInvoice)
        invoice_info = {
            "user_id": str(user["_id"]),
            "parking_lot_id": plot_id,
            "start_time": datetime.utcnow(),
            "end_time": None,
            "unit_price": unit_price,
            "duration": 0.0,
            "total_price": 0.0,
        }
        invoice = self.invoice_repo.createInvoice(invoice_info)

        # 3. Khi xe vào bãi, cập nhật trạng thái ô đỗ (updatePlot)
        self.plot_repo.updatePlot(plot_id, {"status": "occupied"})
        return invoice

    async def updateSensorStatus(self, plot_id, is_leaving: bool):
        # Cập nhật khi xe ra khỏi ô đỗ nhưng chưa ra tới cổng
        status = "available" if is_leaving else "occupied"
        self.plot_repo.updatePlot(plot_id, {"status": status})

    async def checkOut(self, phone, password):
        # 1. User đăng nhập để check-out
        user = self.user_repo.signIn(phone, password)
        if not user:
            raise ValueError("Sai thông tin tài khoản!")

        # 2. Tìm hóa đơn chưa thanh toán của user này
        invoices = self.invoice_repo.getInvoiceByUserId(str(user["_id"]))
        open_invoice = next((i for i in invoices if i["end_time"] is None), None)
        if not open_invoice:
            raise ValueError("Không tìm thấy lượt đỗ xe hiện tại!")

        # 3. Tính toán tiền bạc
        end_time = datetime.utcnow()
        duration_delta = end_time - open_invoice["start_time"]
        # Làm tròn lên số giờ (ví dụ: 1h15p tính là 2h)
        duration_hours = math.ceil(duration_delta.total_seconds() / 3600)
        total_price = duration_hours * open_invoice["unit_price"]

        # 4. Kiểm tra số dư tài khoản
        if user["balance"] < total_price:
            # Gửi thông báo (ở đây ta raise lỗi để Controller bắt)
            raise ValueError(
                f"Tài khoản không đủ tiền! Cần: {total_price}, Hiện có: {user['balance']}"
            )

        # 5. Cập nhật hóa đơn & trừ tiền User
        self.invoice_repo.updateInvoice(
            open_invoice["_id"],
            {
                "end_time": end_time,
                "duration": float(duration_hours),
                "total_price": float(total_price),
            },
        )

        new_balance = user["balance"] - total_price
        self.user_repo.updateBalance(user["_id"], new_balance)

        return {
            "status": "success",
            "total_price": total_price,
            "new_balance": new_balance,
        }
