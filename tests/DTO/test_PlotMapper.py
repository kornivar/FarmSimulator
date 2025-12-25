import unittest
from app.DTO.PlotMapper import PlotMapper
from app.DTO.PlotPurchaseDTO import PlotPurchaseDTO
from app.Models.PlotModel import PlotModel

class TestPlotMapper(unittest.TestCase):

    def test_mapper_creates_plot_with_upgrade(self):
        dto = PlotPurchaseDTO(has_upgrade=True, plot_type="upgrade")

        plot = PlotMapper.from_purchase(dto, plot_index=2)

        self.assertIsInstance(plot, PlotModel)
        self.assertEqual(plot.index, 2)
        self.assertEqual(plot.fertilizer, 5)
        self.assertEqual(plot.state, "locked")

    def test_mapper_creates_plot_without_upgrade(self):
        dto = PlotPurchaseDTO(has_upgrade=False, plot_type="basic")

        plot = PlotMapper.from_purchase(dto, plot_index=1)

        self.assertEqual(plot.fertilizer, 0)
        self.assertEqual(plot.state, "locked")

