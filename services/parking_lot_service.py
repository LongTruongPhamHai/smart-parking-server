class ParkingLotService:
    def __init__(self, repository):
        self.repository = repository

    def add_parking_lot(self, data):
        plot_dict = data.model_dump()
        plot_dict["status"] = "available"  # Luôn mặc định trống khi mới tạo
        return self.repository.addPLot(plot_dict)

    def get_all_plots(self):
        return self.repository.getPLots()

    def get_plot_by_id(self, plot_id: str):
        return self.repository.getPLotById(plot_id)

    def update_plot(self, plot_id: str, info):
        update_data = {k: v for k, v in info.model_dump().items() if v is not None}
        return self.repository.updatePlot(plot_id, update_data)

    def delete_plot(self, plot_id: str):
        return self.repository.deletePlot(plot_id)
