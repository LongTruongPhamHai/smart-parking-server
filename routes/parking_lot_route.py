from fastapi import APIRouter
from controllers.parking_lot_controller import ParkingLotController
from schemas.parking_lot_schema import (
    ParkingLotCreate,
    ParkingLotUpdate,
    ParkingLotResponse,
)

router = APIRouter(
    prefix="/parking-lots",
    tags=["Parking Lots"],
)


@router.post(
    "/",
    response_model=ParkingLotResponse,
    summary="Tạo bãi đỗ xe",
)
async def create_plot(data: ParkingLotCreate):
    return await ParkingLotController.create_plot(data)


@router.get(
    "/",
    response_model=list[ParkingLotResponse],
    summary="Lấy tất cả bãi đỗ",
)
async def get_all_plots():
    return await ParkingLotController.get_all_plots()


@router.get(
    "/{plot_id}",
    response_model=ParkingLotResponse,
    summary="Lấy bãi đỗ theo ID",
)
async def get_plot_by_id(plot_id: str):
    return await ParkingLotController.get_plot_by_id(plot_id)


@router.put(
    "/{plot_id}",
    response_model=ParkingLotResponse,
    summary="Cập nhật bãi đỗ",
)
async def update_plot(plot_id: str, data: ParkingLotUpdate):
    return await ParkingLotController.update_plot(plot_id, data)


@router.delete(
    "/{plot_id}",
    response_model=dict,
    summary="Xóa bãi đỗ",
)
async def delete_plot(plot_id: str):
    return await ParkingLotController.delete_plot(plot_id)
