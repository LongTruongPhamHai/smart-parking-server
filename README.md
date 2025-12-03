```
backend/
│
├── app/
│   ├── main.py              # entrypoint FastAPI
│   ├── models.py            # Beanie models
│   ├── crud.py              # chức năng thao tác DB
│   ├── schemas.py           # Pydantic models
│   ├── database.py          # kết nối MongoDB
│   └── routers/
│       └── users.py         # route API user
│
├── .env                     # config DB
├── requirements.txt
└── README.md
```
