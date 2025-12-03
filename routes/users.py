from fastapi import APIRouter
from schemas import UserCreate, UserOut
from crud import create_user, get_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserOut)
async def api_create_user(user: UserCreate):
    return await create_user(user)


@router.get("/{user_id}", response_model=UserOut)
async def api_get_user(user_id: str):
    return await get_user(user_id)
