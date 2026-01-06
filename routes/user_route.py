from fastapi import APIRouter
from controllers.user_controller import UserController
from schemas.user_schema import UserSignup, UserSignin, UserUpdate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


# ==========================
# Đăng ký / Đăng nhập
# ==========================
@router.post("/signup", response_model=UserResponse)
async def signup(user: UserSignup):
    return await UserController.signup(user)


@router.post("/signin", response_model=UserResponse)
async def signin(user: UserSignin):
    return await UserController.signin(user)


# ==========================
# CRUD người dùng
# ==========================
@router.get("/", response_model=list[UserResponse])
async def get_all_users():
    return await UserController.get_all_users()


@router.get("/by-id/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: str):
    return await UserController.get_user_by_id(user_id)


@router.get("/by-phone/{phone}", response_model=UserResponse)
async def get_user_by_phone(phone: str):
    return await UserController.get_user_by_phone(phone)


# Bỏ /by-email vì không còn email


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, user: UserUpdate):
    return await UserController.update_user(user_id, user)


# ==========================
# Nạp tiền vào tài khoản
# ==========================
@router.post(
    "/{user_id}/add-balance",
    response_model=UserResponse,
    summary="Nạp tiền vào tài khoản người dùng",
)
async def add_balance(user_id: str, amount: float):
    """
    Nạp tiền vào tài khoản user theo user_id.
    - amount: số tiền muốn nạp (phải > 0)
    """
    return await UserController.add_balance(user_id, amount)


@router.delete("/{user_id}")
async def delete_user(user_id: str):
    return await UserController.delete_user(user_id)


# ==========================
# Check-in / Check-out bãi gửi xe
# ==========================
@router.post("/check-in", summary="Người dùng vào bãi gửi xe")
async def check_in(user: UserSignin):
    return await UserController.check_in(user)


@router.post("/check-out", summary="Người dùng ra bãi gửi xe")
async def check_out(user: UserSignin):
    return await UserController.check_out(user)
