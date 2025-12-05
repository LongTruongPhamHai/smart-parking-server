from fastapi import FastAPI
from routes import user_route, wallet_route, vehicle_route, vehicle_type_route

app = FastAPI(title="Smart Parking Backend")

app.include_router(user_route.router)
app.include_router(wallet_route.router)
app.include_router(vehicle_type_route.router)
app.include_router(vehicle_route.router)