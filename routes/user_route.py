from fastapi import APIRouter
from controllers.user_controller import UserController
from schemas.user_schema import UserSignup, UserSignin, UserUpdate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/signup", response_model=UserResponse)
async def signup(user: UserSignup):
    return await UserController.signup(user)

@router.post("/signin", response_model=UserResponse)
async def signin(user: UserSignin):
    return await UserController.signin(user)

@router.get("/", response_model=list[UserResponse])
async def get_all_users():
    return await UserController.get_all_users()

@router.get("/by-id/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: str):
    return await UserController.get_user_by_id(user_id)

@router.get("/by-phone/{phone}", response_model=UserResponse)
async def get_user_by_phone(phone: str):
    return await UserController.get_user_by_phone(phone)

@router.get("/by-email/{email}", response_model=UserResponse)
async def get_user_by_email(email: str):
    return await UserController.get_user_by_email(email)

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, user: UserUpdate):
    return await UserController.update_user(user_id, user)

@router.delete("/{user_id}")
async def delete_user(user_id: str):
    return await UserController.delete_user(user_id)