from .PlotPurchaseDTO import PlotPurchaseDTO
from ..Models.PlotModel import PlotModel

class PlotMapper:

    @staticmethod
    def from_purchase(dto: PlotPurchaseDTO, plot_index: int) -> PlotModel:
        plot = PlotModel(plot_index)

        if dto.has_upgrade:
            plot.fertilizer_charges = 5

        plot.plot_type = dto.plot_type
        return plot