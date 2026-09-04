# ⚙️ Phân hệ Backend (Smart Parking Server)

> **Dự án:** Hệ thống quản lý bãi đỗ xe thông minh (Đại học Thuỷ Lợi)  
> **Vai trò:** Backend Server cung cấp RESTful APIs xử lý toàn bộ logic hệ thống

---

## 🛠 Công nghệ sử dụng

- **Ngôn ngữ:** Python 3.10+
- **Framework:** FastAPI
- **Cơ sở dữ liệu:** MongoDB (Async driver: `motor`)
- **ASGI Server:** Uvicorn
- **Validation:** Pydantic v2

---

## 📂 Cấu trúc thư mục (Architecture)

Server được tổ chức theo kiến trúc **Controller-Service-Repository** để đảm bảo clean code và dễ dàng mở rộng:

```
smart-parking-server/
├── controllers/         # API logic - xử lý request/response
├── services/            # Business logic - xử lý nghiệp vụ
├── repositories/        # Data access layer - CRUD MongoDB
├── models/              # Pydantic models - định nghĩa data structure
├── schemas/             # Request/Response schemas - validation
├── routes/              # API routers - định nghĩa endpoints
├── core/                # Config và utilities
├── db.py                # MongoDB connection
├── main.py              # FastAPI app entry point
└── requirements.txt     # Python dependencies
```

**Luồng xử lý request:**

```
Client → Route → Controller → Service → Repository → MongoDB
                                ↓
Client ← Response ← Schema ← Model
```

---

## 🔌 API Endpoints

### 🔐 Users (`/users`)

- `POST /users/signup` - Đăng ký tài khoản mới (Customer)
- `POST /users/signin` - Đăng nhập
- `GET /users/` - Lấy danh sách tất cả users (Admin)
- `GET /users/by-id/{user_id}` - Lấy thông tin user theo ID
- `PUT /users/{user_id}` - Cập nhật thông tin user
- `DELETE /users/{user_id}` - Xóa user
- `PUT /users/{user_id}/add-balance` - Nạp tiền vào tài khoản
- `PUT /users/{user_id}/change-password` - Đổi mật khẩu

### 🚗 Parking Lots (`/parking-lots`)

- `GET /parking-lots/` - Lấy danh sách tất cả parking slots
- `GET /parking-lots/{slot_id}` - Lấy thông tin slot theo ID
- `PUT /parking-lots/{slot_id}` - Cập nhật thông tin slot
- `POST /parking-lots/check-in` - Check-in xe vào bãi
- `POST /parking-lots/check-out/{invoice_id}` - Check-out xe ra bãi

### 💰 Invoices (`/invoices`)

- `GET /invoices/` - Lấy tất cả invoices (Admin)
- `GET /invoices/user/{user_id}` - Lấy invoices của user cụ thể
- `POST /invoices/check-in` - Tạo invoice mới (xe vào)
- `POST /invoices/check-out/{invoice_id}` - Hoàn thành invoice (xe ra + thanh toán)

### 🔔 Notifications (`/api/notifications`)

- `GET /api/notifications/` - Lấy notifications cho Admin (Activity Logs)
- `GET /api/notifications/user/{user_id}` - Lấy notifications của user
- `POST /api/notifications/create` - Tạo notification cho 1 user
- `POST /api/notifications/broadcast` - Broadcast notification (all/admins)
- `PUT /api/notifications/{notification_id}/read` - Đánh dấu đã đọc
- `DELETE /api/notifications/{notification_id}` - Xóa notification

---

## 🚀 Hướng dẫn cài đặt và khởi chạy

**Bước 1: Cài đặt thư viện**  
Yêu cầu hệ thống đã cài đặt Python. Mở terminal tại thư mục này và chạy:

```bash
pip install -r requirements.txt
```

**Bước 2: Cấu hình môi trường**  
Tuỳ chỉnh các thông số trong file `core/config.py` (hoặc tạo file `.env` nếu có) để kết nối với cơ sở dữ liệu MongoDB.

**Bước 3: Khởi động Server**  
Chạy lệnh sau để khởi động Backend ở chế độ phát triển (auto-reload):

```bash
uvicorn main:app --reload
```

Theo mặc định, Server sẽ chạy tại địa chỉ: `http://127.0.0.1:8000`.

**Bước 4: Xem tài liệu API (Swagger UI)**  
Truy cập vào trình duyệt: `http://127.0.0.1:8000/docs` để trải nghiệm trực tiếp giao diện Swagger UI tự động sinh ra bởi FastAPI.

---

## 📊 Database Collections

Hệ thống sử dụng 4 collections chính trong MongoDB:

### 1. `users`

```json
{
  "_id": ObjectId,
  "name": "string",
  "phone": "string",
  "email": "string",
  "password": "hashed_string",
  "role": "Admin" | "Customer",
  "balance": float
}
```

### 2. `parking_lots`

```json
{
  "_id": ObjectId,
  "name": "string",
  "status": "available" | "occupied",
  "unit_price": float
}
```

### 3. `invoices`

```json
{
  "_id": ObjectId,
  "user_id": "string",
  "parking_lot_id": "string",
  "start_time": datetime,
  "end_time": datetime | null,
  "duration": float,
  "total_price": float,
  "unit_price": float,
  "status": "active" | "completed"
}
```

### 4. `notifications`

```json
{
  "_id": ObjectId,
  "user_id": "string",
  "title": "string",
  "message": "string",
  "type": "info" | "success" | "warning" | "error" | "fire" | "gas",
  "is_read": boolean,
  "created_at": datetime
}
```

---

## 🔔 Hệ thống Notification

**Cơ chế hoạt động:**

- Notifications lưu trong MongoDB collection `notifications`
- Mỗi notification gắn với `user_id` (người nhận)
- Admin xem logs qua `/api/notifications/` (chỉ hiển thị notifications gửi tới Admin)

**Các event tự động tạo notification:**

_Gửi tới Admin:_

- Xe check-in vào bãi
- Xe check-out khỏi bãi
- Cảnh báo cháy (fire alert)
- Cảnh báo khí gas (gas alert)

_Gửi tới Customer (dữ liệu lưu, chưa hiển thị UI):_

- Thông báo check-in thành công
- Thông báo check-out + tổng tiền
- Cảnh báo cháy/gas (broadcast)

**~~Email Notifications~~**  
Đã loại bỏ - thay bằng in-app notifications. Code liên quan đã comment trong `services/user_service.py`.

---

## 🐛 Troubleshooting

**Lỗi "Connection refused":**

- Kiểm tra MongoDB: `mongod --version`
- Kiểm tra connection string trong `db.py`

**CORS errors:**

- Kiểm tra CORS middleware trong `main.py`

**Port 8000 đã sử dụng:**

- Đổi port: `uvicorn main:app --port 8001`

---

## 📝 Lưu ý

- Database operations đều **async** (dùng `await`)
- Timezone: UTC trong DB, convert GMT+7 ở Frontend
- Chưa có authentication middleware (JWT/session)
