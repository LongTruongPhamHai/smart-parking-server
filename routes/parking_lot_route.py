# routers/parking_lot_router.py
from fastapi import APIRouter
from controllers.parking_lot_controller import ParkingLotController
from schemas.parking_lot_schema import (
    ParkingLotCreate,
    ParkingLotUpdate,
    ParkingLotResponse,
)

router = APIRouter(prefix="/parking_lots", tags=["Parking_Lot"])


@router.post("/", response_model=ParkingLotResponse)
async def add_plot(data: ParkingLotCreate):
    """Tương ứng addPlot(info) - Admin thêm ô đỗ mới"""
    return await ParkingLotController.add_plot(data)


@router.get("/", response_model=list[ParkingLotResponse])
async def get_plots():
    """Tương ứng getPlots() - Lấy danh sách tất cả ô đỗ"""
    return await ParkingLotController.get_all_plots()


@router.get("/{plot_id}", response_model=ParkingLotResponse)
async def get_plot_by_id(plot_id: str):
    """Tương ứng getPlotById(id) - Lấy chi tiết 1 ô đỗ"""
    return await ParkingLotController.get_plot_by_id(plot_id)


@router.put("/{plot_id}", response_model=ParkingLotResponse)
async def update_plot(plot_id: str, data: ParkingLotUpdate):
    """Tương ứng updatePlot(info) - Cập nhật thông tin/trạng thái ô đỗ"""
    return await ParkingLotController.update_plot(plot_id, data)


@router.delete("/{plot_id}")
async def delete_plot(plot_id: str):
    """Tương ứng deletePlot(id) - Xóa ô đỗ khỏi hệ thống"""
    return await ParkingLotController.delete_plot(plot_id)
