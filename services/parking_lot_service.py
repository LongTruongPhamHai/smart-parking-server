# services/parking_lot_service.py
from repositories.parking_lot_repository import ParkingLotRepository


class ParkingLotService:
    @staticmethod
    async def add_plot(info: dict):
        return await ParkingLotRepository.add(info)

    @staticmethod
    async def get_plots():
        plots = await ParkingLotRepository.get_all()
        return [{"id": str(p["_id"]), **p} for p in plots]

    @staticmethod
    async def get_plot_by_id(plot_id: str):
        plot = await ParkingLotRepository.get_by_id(plot_id)
        if plot:
            plot["id"] = str(plot["_id"])
        return plot

    @staticmethod
    async def update_plot(plot_id: str, info: dict):
        return await ParkingLotRepository.update(plot_id, info)

    @staticmethod
    async def delete_plot(plot_id: str):
        return await ParkingLotRepository.delete(plot_id)
