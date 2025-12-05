from fastapi import FastAPI
from routes import user_route, wallet_route

app = FastAPI(title="Smart Parking Backend")

app.include_router(user_route.router)
app.include_router(wallet_route.router)
# Run: uvicorn main:app --reload