CREATE TABLE users (
    id SERIAL PRIMARY KEY,                      -- Tự động tăng
    name VARCHAR(100) NOT NULL,                 -- Tên người dùng
    email VARCHAR(150) UNIQUE,                  -- Email duy nhất
    phone VARCHAR(20) UNIQUE,                   -- Số điện thoại duy nhất
    role VARCHAR(50) DEFAULT 'customer',            -- Vai trò (user/admin)
    password VARCHAR(255) NOT NULL,             -- Mật khẩu đã hash
    created_at TIMESTAMP DEFAULT NOW(),         -- Ngày tạo
    updated_at TIMESTAMP DEFAULT NOW()          -- Ngày cập nhật
);

UPDATE users
SET role = 'customer'
WHERE role = 'user';

ALTER TABLE users
ALTER COLUMN role SET DEFAULT 'customer';



CREATE TABLE wallets (
    id SERIAL PRIMARY KEY,             								-- id tự tăng
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,  	-- liên kết với bảng users
    balance NUMERIC(12,2) DEFAULT 0,  								-- số dư, mặc định 0
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE vehicle_types (
    id SERIAL PRIMARY KEY,         -- id tự tăng
    name VARCHAR(100) NOT NULL     -- tên loại xe (Ví dụ: "Xe máy", "Ô tô")
);

CREATE TABLE vehicles (
    id SERIAL PRIMARY KEY,                                							-- id tự tăng
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,  					-- liên kết với bảng users
    license_plate VARCHAR(20) UNIQUE NOT NULL,           							-- biển số xe duy nhất
    vehicle_type_id INT NOT NULL REFERENCES vehicle_types(id) ON DELETE SET NULL, 	-- liên kết loại xe
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE parking_lot (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE parking_price (
    id SERIAL PRIMARY KEY,
    vehicle_type_id INT NOT NULL REFERENCES vehicle_types(id) ON DELETE CASCADE,
    parking_lot_id INT NOT NULL REFERENCES parking_lot(id) ON DELETE CASCADE,
    price NUMERIC(12,2) NOT NULL,          							-- đơn giá
    start_time TIME NOT NULL,              							-- giờ bắt đầu áp dụng
    end_time TIME NOT NULL,                							-- giờ kết thúc áp dụng
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(vehicle_type_id, parking_lot_id, start_time, end_time) 	-- tránh trùng khung giờ
);

CREATE TABLE parking_invoice (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    vehicle_id INT NOT NULL REFERENCES vehicles(id) ON DELETE CASCADE,
    wallet_id INT NOT NULL REFERENCES wallets(id) ON DELETE CASCADE,
    parking_lot_id INT NOT NULL REFERENCES parking_lot(id) ON DELETE CASCADE,
    start_time TIMESTAMP NOT NULL,      							-- thời gian vào bãi
    end_time TIMESTAMP,                 							-- thời gian rời bãi
    price_id INT REFERENCES parking_price(id) ON DELETE SET NULL,
    duration INTERVAL,                  							-- thời gian đỗ
    total_price NUMERIC(12,2),          							-- tổng tiền thanh toán
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO users (name, email, phone, role, password)
VALUES
    ('Alice Nguyen', 'alice@example.com', '0901234567', 'customer', '111111'),
    ('Bob Tran', 'bob@example.com', '0902345678', 'admin', '111111'),
    ('Charlie Le', 'charlie@example.com', '0903456789', 'user', '111111');

SELECT * FROM users;
