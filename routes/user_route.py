from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user_schema import UserCreate, UserLogin, UserUpdate, UserOut
from controllers.user_controller import UserController
from db import get_db
from typing import List

router = APIRouter()

@router.post("/signup", response_model=UserOut)
async def signup(user: UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await UserController.get_users(db)
    for u in existing:
        if u.email == user.email:
            raise HTTPException(status_code=400, detail="Email already exists")
    return await UserController.signup(user, db)

@router.post("/signin", response_model=UserOut)
async def signin(login: UserLogin, db: AsyncSession = Depends(get_db)):
    user = await UserController.signin(login, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

@router.get("/", response_model=List[UserOut])
async def get_users(db: AsyncSession = Depends(get_db)):
    return await UserController.get_users(db)

@router.get("/{user_id}", response_model=UserOut)
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await UserController.get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserOut)
async def update_user(user_id: int, data: UserUpdate, db: AsyncSession = Depends(get_db)):
    user = await UserController.update(user_id, data, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await UserController.delete(user_id, db)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
