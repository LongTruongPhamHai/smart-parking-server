```
project/
│
├─ venv/
├─ main.py
├─ db.py
├─ .env
├─ requirements.txt
│
├─ sql/
│   └─ init.sql
│
├─ models/
│   ├─ parking_lot_model.py
│   ├─ parking_transaction_model.py
│   ├─ parking_price_model.py
│   ├─ wallet_model.py
│   ├─ vehicle_model.py
│   ├─ vehicle_type_model.py
│   └─ user_model.py
│
├─ repositories/
│   ├─ parking_lot_repository.py
│   ├─ parking_transaction_repository.py
│   ├─ parking_price_repository.py
│   ├─ wallet_repository.py
│   ├─ vehicle_repository.py
│   ├─ vehicle_type_repository.py
│   └─ user_repository.py
│
├─ services/
│   └─ user_service.py
│
├─ controllers/
│   └─ user_controller.py
│
├─ routes/
│   └─ user_route.py
│
└─ schemas/
    └─ user_schema.py

```

pip install -r requirements.txt

uvicorn main:app --reload
