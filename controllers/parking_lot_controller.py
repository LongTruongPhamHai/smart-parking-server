from fastapi import HTTPException
from schemas.parking_lot_schema import ParkingLotResponse


class ParkingLotController:
    def __init__(self, service):
        self.service = service

    def add_plot(self, data):
        new_plot = self.service.add_parking_lot(data)
        return ParkingLotResponse(**new_plot.to_dict())

    def get_plots(self):
        plots = self.service.get_all_plots()
        return [ParkingLotResponse(**p.to_dict()) for p in plots]

    def get_plot(self, plot_id: str):
        plot = self.service.get_plot_by_id(plot_id)
        if not plot:
            raise HTTPException(status_code=404, detail="Slot not found")
        return ParkingLotResponse(**plot.to_dict())

    def update_plot(self, plot_id: str, info):
        if not self.service.update_plot(plot_id, info):
            raise HTTPException(status_code=404, detail="Update failed")
        return {"message": "Parking slot updated successfully"}

    def delete_plot(self, plot_id: str):
        if not self.service.delete_plot(plot_id):
            raise HTTPException(status_code=404, detail="Slot not found")
        return {"message": "Parking slot deleted"}
