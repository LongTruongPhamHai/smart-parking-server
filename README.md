# 🚗 Smart Parking Backend

Backend API cho **Hệ thống Bãi đỗ xe Thông minh (Smart Parking)** được xây dựng với:

- **FastAPI**
- **MongoDB** (Motor hoặc PyMongo)
- **Pydantic**
- **Uvicorn**
- **Python 3.10+**

Hệ thống hỗ trợ quản lý người dùng, phương tiện, ví điện tử, bãi đỗ xe, giá theo loại xe và các phiên gửi xe.

---

## 📁 Cấu trúc dự án

```
server/
│
├─ venv/                          # Virtual environment
├─ main.py                        # Entry chính của ứng dụng FastAPI
├─ db.py                          # Cấu hình MongoDB (Motor / PyMongo)
├─ .env                           # Biến môi trường
├─ requirements.txt               # Danh sách thư viện cần cài đặt
│
├─ models/                        # Định nghĩa cấu trúc dữ liệu (MongoDB schema)
│   ├─ __init__.py
│   ├─ wallet_model.py
│   ├─ vehicle_model.py
│   ├─ vehicle_type.py
│   ├─ parking_lot_model.py
│   ├─ parking_price_model.py
│   ├─ parking_transaction_model.py
│   └─ user_model.py
│
├─ repositories/                  # Layer truy cập dữ liệu MongoDB
│   ├─ __init__.py
│   └─ user_repository.py
│
├─ services/                      # Business logic
│   ├─ __init__.py
│   └─ user_service.py
│
├─ controllers/                   # Xử lý request/response
│   ├─ __init__.py
│   └─ user_controller.py
│
├─ routes/                        # Định nghĩa API endpoint
│   ├─ __init__.py
│   └─ user_route.py
│
└─ schemas/                       # Pydantic schema validate dữ liệu request
    ├─ __init__.py
    └─ user_schema.py
```

---

## 📦 Yêu cầu môi trường

Các thư viện chính:

```
fastapi
uvicorn
pydantic
pydantic[email]
python-dotenv
motor   # hoặc pymongo
```

Cài đặt tất cả:

```bash
pip install -r requirements.txt
```

---

## 🔐 Biến môi trường

Tạo file **`.env`**:

```
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=smart_parking_db
SECRET_KEY=your_secret_key
```

Nếu dùng MongoDB Atlas:

```
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net
```

---

## 🗄️ Thiết lập cơ sở dữ liệu

MongoDB **không yêu cầu tạo bảng trước**.
Các collection sẽ tự tạo khi có dữ liệu.

Kiểm tra kết nối bằng:

```bash
mongosh
use smart_parking_db
show collections
```

---

## 🚀 Chạy API

Chạy server FastAPI:

```bash
uvicorn main:app --reload
```

Truy cập API:

```
http://127.0.0.1:8000
```

---

## 📘 API Endpoints

- **User** – `/users`

  - Đăng ký
  - Đăng nhập
  - Xem/ cập nhật thông tin người dùng

Có thể mở rộng:

- `/vehicles` – Quản lý phương tiện
- `/wallets` – Ví điện tử, giao dịch
- `/parking-lots` – Bãi đỗ xe
- `/parking-sessions` – Phiên gửi xe
- `/transactions` – Hóa đơn/ghi nhận thanh toán

Tài liệu Swagger:

```
http://127.0.0.1:8000/docs
```

---

## 📝 Lưu ý phát triển

- Dùng **venv** để tách môi trường.
- MongoDB không cần migration, nhưng **nên**:

  - Define schema bằng Pydantic (validate input)
  - Chuẩn hóa dữ liệu trong model Python

- **repositories**: xử lý truy vấn MongoDB
- **services**: logic nghiệp vụ
- **controllers**: điều phối request – service – response
- **routes**: tổ chức endpoint rõ ràng theo module
