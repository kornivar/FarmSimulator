import unittest
from app.DTO.PlotPurchaseDTO import PlotPurchaseDTO

class TestPlotPurchaseDTO(unittest.TestCase):

    def test_dto_fields_are_set(self):
        dto = PlotPurchaseDTO(has_upgrade=True, plot_type="upgrade")

        self.assertTrue(dto.has_upgrade)
        self.assertEqual(dto.plot_type, "upgrade")