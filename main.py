from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.user_route import router as user_router
from db import engine
from models.user_model import Base

app = FastAPI(title="User Management API")

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # cho phép domain frontend
    allow_credentials=True,
    allow_methods=["*"],         # cho phép GET, POST, PUT, DELETE...
    allow_headers=["*"],         # cho phép mọi header
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(user_router, prefix="/users", tags=["Users"])
