from repositories.parking_lot_repository import ParkingLotRepository


class ParkingLotService:
    @staticmethod
    async def add_parking_lot(plot_data: dict):
        # Bạn có thể thêm logic kiểm tra tên bãi xe đã tồn tại chưa nếu cần
        return await ParkingLotRepository.addPLot(plot_data)

    @staticmethod
    async def get_all_parking_lots():
        return await ParkingLotRepository.getPLots()

    @staticmethod
    async def get_parking_lot_by_id(plot_id: str):
        plot = await ParkingLotRepository.getPLotById(plot_id)
        if not plot:
            raise ValueError("Parking lot not found")
        return plot

    @staticmethod
    async def update_parking_lot(plot_id: str, update_data: dict):
        # Loại bỏ các giá trị None để tránh ghi đè dữ liệu cũ bằng null
        clean_data = {k: v for k, v in update_data.items() if v is not None}
        return await ParkingLotRepository.updatePlot(plot_id, clean_data)

    @staticmethod
    async def delete_parking_lot(plot_id: str):
        return await ParkingLotRepository.deletePlot(plot_id)
