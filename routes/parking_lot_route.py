from fastapi import APIRouter
from db import db
from repositories.parking_lot_repository import ParkingLotRepository
from services.parking_lot_service import ParkingLotService
from controllers.parking_lot_controller import ParkingLotController
from schemas.parking_lot_schema import (
    ParkingLotCreate,
    ParkingLotUpdate,
    ParkingLotResponse,
)

router = APIRouter(prefix="/parking-lots", tags=["Parking Lots"])

# Khởi tạo các lớp
repo = ParkingLotRepository(db["parking_lots"])
service = ParkingLotService(repo)
controller = ParkingLotController(service)


@router.post("/", response_model=ParkingLotResponse)
def add_plot(data: ParkingLotCreate):
    return controller.add_plot(data)


@router.get("/", response_model=list[ParkingLotResponse])
def get_all_plots():
    return controller.get_plots()


@router.get("/{plot_id}", response_model=ParkingLotResponse)
def get_plot(plot_id: str):
    return controller.get_plot(plot_id)


@router.put("/{plot_id}")
def update_plot(plot_id: str, info: ParkingLotUpdate):
    return controller.update_plot(plot_id, info)


@router.delete("/{plot_id}")
def delete_plot(plot_id: str):
    return controller.delete_plot(plot_id)
