from fastapi import FastAPI
from routes.user_route import router as user_router
from db import engine
from models.user_model import Base

app = FastAPI(title="User Management API")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(user_router, prefix="/users", tags=["Users"])
