from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import (
    invoice_route,
    user_route,
    parking_lot_route,
)

app = FastAPI()

# Cấu hình CORS
origins = ["*"]  # Cho phép tất cả


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Cho phép các origin này
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả method: GET, POST, PUT, DELETE...
    allow_headers=["*"],  # Cho phép tất cả headers
)


@app.get("/")
async def root():
    return {"message": "Backend is running!"}


app.include_router(user_route.router)
app.include_router(parking_lot_route.router)
app.include_router(invoice_route.router)
