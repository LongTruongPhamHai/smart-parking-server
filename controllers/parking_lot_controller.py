from fastapi import HTTPException
from services.parking_lot_service import ParkingLotService
from schemas.parking_lot_schema import (
    ParkingLotCreate,
    ParkingLotUpdate,
    ParkingLotResponse,
)
from models.parking_lot_model import ParkingLotModel


class ParkingLotController:

    @staticmethod
    async def create_plot(data: ParkingLotCreate) -> ParkingLotResponse:
        plot: ParkingLotModel = await ParkingLotService.create_plot(
            data.dict(exclude_unset=True)
        )
        return ParkingLotResponse(**plot.to_dict())

    @staticmethod
    async def get_all_plots() -> list[ParkingLotResponse]:
        plots: list[ParkingLotModel] = await ParkingLotService.get_all_plots()
        return [ParkingLotResponse(**plot.to_dict()) for plot in plots]

    @staticmethod
    async def get_plot_by_id(plot_id: str) -> ParkingLotResponse:
        plot = await ParkingLotService.get_plot_by_id(plot_id)
        if plot is None:
            raise HTTPException(status_code=404, detail="Parking lot not found")
        return ParkingLotResponse(**plot.to_dict())

    @staticmethod
    async def update_plot(plot_id: str, data: ParkingLotUpdate) -> ParkingLotResponse:
        plot = await ParkingLotService.update_plot(
            plot_id, data.dict(exclude_unset=True)
        )
        if plot is None:
            raise HTTPException(status_code=404, detail="Parking lot not found")
        return ParkingLotResponse(**plot.to_dict())

    @staticmethod
    async def delete_plot(plot_id: str) -> dict:
        deleted = await ParkingLotService.delete_plot(plot_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Parking lot not found")
        return {"message": "Parking lot deleted successfully"}
