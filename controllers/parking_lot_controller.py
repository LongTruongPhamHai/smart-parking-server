from fastapi import HTTPException
from services.parking_lot_service import ParkingLotService
from schemas.parking_lot_schema import (
    ParkingLotCreate,
    ParkingLotUpdate,
    ParkingLotResponse,
)


class ParkingLotController:
    @staticmethod
    async def add_parking_lot(plot_data: ParkingLotCreate) -> ParkingLotResponse:
        try:
            new_plot = await ParkingLotService.add_parking_lot(plot_data.dict())
            return ParkingLotResponse(**new_plot.to_dict())
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def get_all_parking_lots() -> list[ParkingLotResponse]:
        plots = await ParkingLotService.get_all_parking_lots()
        return [ParkingLotResponse(**p.to_dict()) for p in plots]

    @staticmethod
    async def get_parking_lot_by_id(plot_id: str) -> ParkingLotResponse:
        try:
            plot = await ParkingLotService.get_parking_lot_by_id(plot_id)
            return ParkingLotResponse(**plot.to_dict())
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    @staticmethod
    async def update_parking_lot(
        plot_id: str, update_data: ParkingLotUpdate
    ) -> ParkingLotResponse:
        updated = await ParkingLotService.update_parking_lot(
            plot_id, update_data.dict(exclude_unset=True)
        )
        if not updated:
            raise HTTPException(status_code=404, detail="Parking lot not found")
        return ParkingLotResponse(**updated.to_dict())

    @staticmethod
    async def delete_parking_lot(plot_id: str) -> dict:
        deleted = await ParkingLotService.delete_parking_lot(plot_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Parking lot not found")
        return {"message": "Parking lot deleted successfully"}
