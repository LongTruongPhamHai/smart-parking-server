from repositories.parking_lot_repository import ParkingLotRepository
from models.parking_lot_model import ParkingLotModel


class ParkingLotService:
    @staticmethod
    async def create_plot(data: dict) -> ParkingLotModel:
        """
        Tạo ô đỗ mới
        """
        return await ParkingLotRepository.create(data)

    @staticmethod
    async def get_all_plots() -> list[ParkingLotModel]:
        """
        Lấy danh sách tất cả ô đỗ
        """
        return await ParkingLotRepository.getAll()

    @staticmethod
    async def get_plot_by_id(plot_id: str) -> ParkingLotModel | None:
        """
        Lấy chi tiết một ô đỗ theo ID
        """
        return await ParkingLotRepository.getById(plot_id)

    @staticmethod
    async def update_plot(plot_id: str, data: dict) -> ParkingLotModel | None:
        """
        Cập nhật thông tin / trạng thái ô đỗ
        """
        return await ParkingLotRepository.update(plot_id, data)

    @staticmethod
    async def delete_plot(plot_id: str) -> bool:
        """
        Xóa ô đỗ
        """
        return await ParkingLotRepository.delete(plot_id)
