from fastapi import APIRouter
from controllers.parking_lot_controller import ParkingLotController
from schemas.parking_lot_schema import (
    ParkingLotCreate,
    ParkingLotUpdate,
    ParkingLotResponse,
)

router = APIRouter(prefix="/parking-lots", tags=["Parking Lots"])


@router.post("/", response_model=ParkingLotResponse)
async def add_parking_lot(plot: ParkingLotCreate):
    return await ParkingLotController.add_parking_lot(plot)


@router.get("/", response_model=list[ParkingLotResponse])
async def get_all_parking_lots():
    return await ParkingLotController.get_all_parking_lots()


@router.get("/{plot_id}", response_model=ParkingLotResponse)
async def get_parking_lot_by_id(plot_id: str):
    return await ParkingLotController.get_parking_lot_by_id(plot_id)


@router.put("/{plot_id}", response_model=ParkingLotResponse)
async def update_parking_lot(plot_id: str, plot: ParkingLotUpdate):
    return await ParkingLotController.update_parking_lot(plot_id, plot)


@router.delete("/{plot_id}")
async def delete_parking_lot(plot_id: str):
    return await ParkingLotController.delete_parking_lot(plot_id)
