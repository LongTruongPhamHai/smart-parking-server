from fastapi import APIRouter, Query
from controllers.user_controller import UserController
from schemas.user_schema import UserSignup, UserSignin, UserUpdate, UserResponse
from pydantic import BaseModel

router = APIRouter(prefix="/users", tags=["Users"])


class CheckInResponse(BaseModel):
    message: str
    invoice_id: str
    start_time: str | None


class CheckOutResponse(BaseModel):
    message: str
    invoice_id: str
    start_time: str | None
    end_time: str | None
    total_amount: float


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


@router.put("/{user_id}/update-email", response_model=UserResponse)
async def update_email(
    user_id: str, new_email: str = Query(..., description="Email mới")
):
    return await UserController.update_email(user_id, new_email)


@router.post(
    "/{user_id}/add-balance",
    response_model=UserResponse,
    summary="Nạp tiền vào tài khoản người dùng",
)
async def add_balance(
    user_id: str, amount: float = Query(..., description="Số tiền nạp vào (>0)")
):
    return await UserController.add_balance(user_id, amount)


@router.put(
    "/{user_id}/update-balance", response_model=UserResponse, summary="Cập nhật số dư"
)
async def update_balance(
    user_id: str, amount: float = Query(..., description="Số tiền thay đổi (có thể âm)")
):
    return await UserController.update_balance(user_id, amount)


@router.delete("/{user_id}")
async def delete_user(user_id: str):
    return await UserController.delete_user(user_id)


@router.post(
    "/check-in", response_model=CheckInResponse, summary="Người dùng vào bãi gửi xe"
)
async def check_in(user: UserSignin):
    return await UserController.check_in(user)


@router.post(
    "/check-out", response_model=CheckOutResponse, summary="Người dùng ra bãi gửi xe"
)
async def check_out(user: UserSignin):
    return await UserController.check_out(user)


@router.post("/fire", summary="Gửi email cảnh báo cháy")
async def fire_alert():
    return await UserController.send_fire_alert()


@router.post("/gas", summary="Gửi email cảnh báo khí GAS")
async def gas_alert():
    return await UserController.send_gas_alert()
