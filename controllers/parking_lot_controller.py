# controllers/parking_lot_controller.py
from fastapi import HTTPException
from services.parking_lot_service import ParkingLotService


class ParkingLotController:
    @staticmethod
    async def add_plot(data):
        plot_id = await ParkingLotService.add_plot(data.model_dump())
        return {**data.model_dump(), "id": plot_id}

    @staticmethod
    async def get_all_plots():
        return await ParkingLotService.get_plots()

    @staticmethod
    async def get_plot_by_id(plot_id: str):
        plot = await ParkingLotService.get_plot_by_id(plot_id)
        if not plot:
            raise HTTPException(status_code=404, detail="Plot not found")
        return plot

    @staticmethod
    async def update_plot(plot_id: str, data):
        await ParkingLotService.update_plot(plot_id, data.model_dump(exclude_none=True))
        return await ParkingLotService.get_plot_by_id(plot_id)

    @staticmethod
    async def delete_plot(plot_id: str):
        await ParkingLotService.delete_plot(plot_id)
        return {"message": "Deleted successfully"}
