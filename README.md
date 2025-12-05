# Smart Parking Backend

API backend cho **Hệ thống Bãi đỗ xe Thông minh (Smart Parking)** sử dụng **Python**, **FlaskAPI** và **PostgreSQL**.

---

## Cấu trúc dự án

```
server/
│
├─ venv/                      # Virtual environment
├─ main.py                     # Entry điểm ứng dụng
├─ db.py                       # Cấu hình kết nối cơ sở dữ liệu
├─ .env                        # Biến môi trường
├─ requirements.txt            # Thư viện Python cần cài đặt
│
├─ models/                     # Các model SQLAlchemy
│   ├─ __init__.py
│   └─ user_model.py
│
├─ repositories/               # Lớp truy xuất dữ liệu
│   ├─ __init__.py
│   └─ user_repository.py
│
├─ services/                   # Logic nghiệp vụ
│   ├─ __init__.py
│   └─ user_service.py
│
├─ controllers/                # Controller xử lý request
│   ├─ __init__.py
│   └─ user_controller.py
│
├─ routes/                     # Định nghĩa API route
│   ├─ __init__.py
│   └─ user_route.py
│
└─ schemas/                    # Schema Pydantic để validate dữ liệu
    ├─ __init__.py
    └─ user_schema.py
```

---

## Yêu cầu

- Python 3.10+
- PostgreSQL 14+
- FlaskAPI
- SQLAlchemy
- Pydantic
- Uvicorn (cho môi trường phát triển)

Cài đặt các thư viện:

```bash
pip install -r requirements.txt
```

---

## Biến môi trường

Tạo file `.env` trong thư mục gốc:

```
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/smart_parking_db
SECRET_KEY=your_secret_key
```

> Thay `username`, `password` và `smart_parking_db` bằng thông tin PostgreSQL của bạn.

---

## Thiết lập cơ sở dữ liệu

1. Tạo cơ sở dữ liệu PostgreSQL:

```sql
CREATE DATABASE smart_parking_db;
```

2. Khởi tạo bảng bằng file SQL:

```bash
psql -U username -d smart_parking_db -f sql/init.sql
```

---

## Chạy API

Chạy server phát triển:

```bash
uvicorn main:app --reload
```

API sẽ truy cập được tại:

```
http://127.0.0.1:8000
```

---

## Endpoint API

- **User**: `/users`

  - Signup, login, quản lý thông tin người dùng

- Các module khác có thể thêm cho: vehicles, wallets, parking lots, transactions.

> Tài liệu Swagger có thể xem tại:
> `http://127.0.0.1:8000/docs`

---

## Lưu ý khi phát triển

- Sử dụng `venv` để quản lý thư viện riêng cho dự án.
- Lưu các script SQL trong thư mục `sql/` để dễ quản lý version.
- `repositories` dùng cho truy xuất dữ liệu, `services` cho logic nghiệp vụ.
- `controllers` xử lý request và định dạng response.
- `routes` để tổ chức các API endpoint.
