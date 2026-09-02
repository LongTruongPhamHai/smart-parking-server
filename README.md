# ⚙️ Phân hệ Backend (Smart Parking Server)

> **Dự án:** Hệ thống quản lý bãi đỗ xe thông minh (Đại học Thuỷ Lợi)  
> **Vai trò:** Backend Server cung cấp RESTful APIs xử lý toàn bộ logic hệ thống.

---

## 🛠 Công nghệ sử dụng

- **Ngôn ngữ:** Python 3.10+
- **Framework:** FastAPI
- **Cơ sở dữ liệu:** MongoDB (Sử dụng thư viện `motor` để giao tiếp bất đồng bộ)
- **Máy chủ ASGI:** Uvicorn

---

## 📂 Cấu trúc thư mục (Architecture)

Server được tổ chức theo kiến trúc Controller-Service-Repository để đảm bảo clean code và dễ dàng mở rộng:
- `controllers/`: Chứa các endpoint API (Routers), tiếp nhận Request và trả về Response.
- `services/`: Chứa các logic nghiệp vụ (Business logic) như xử lý tính toán tiền, check-in, check-out.
- `repositories/`: Chịu trách nhiệm trực tiếp giao tiếp với Database MongoDB (CRUD).
- `models/`: Định nghĩa các Pydantic Models để ánh xạ với MongoDB Documents.
- `schemas/`: Định nghĩa các Pydantic Schemas dùng để Validate dữ liệu đầu vào/ra (Request/Response).

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
