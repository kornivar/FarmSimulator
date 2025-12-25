import unittest

from app.Models.GModel import GModel
from app.Models.PlotModel import PlotModel
from app.Models.Plant import Plant


class TestGModel(unittest.TestCase):
    def setUp(self):
        self.model = GModel()

    def test_initial_state_defaults(self):
        self.assertEqual(self.model.money, 30)
        self.assertEqual(self.model.fertilizer, 0)

        self.assertIn(1, self.model.buy_prices)
        self.assertIn(2, self.model.buy_prices)
        self.assertIn(3, self.model.buy_prices)

        self.assertEqual(len(self.model.plants), 3)
        self.assertEqual(len(self.model.plots), 5)

        self.assertIsInstance(self.model.missions, dict)
        self.assertGreaterEqual(len(self.model.missions), 5)

        self.assertEqual(self.model.barn, {})

        for plot in self.model.plots:
            self.assertEqual(plot.state, "locked")
            self.assertIsNone(plot.plant)
            self.assertEqual(plot.remaining, 0)

    def test_plot_init_without_fertilizer_sets_full_duration(self):
        idx = 0
        plant = self.model.plants[0]  

        self.model.plots[idx].fertilizer_charges = 0

        self.model.plot_init(plant.id, idx, fertilizer_available=False)

        plot = self.model.plots[idx]
        self.assertEqual(plot.state, "growing")
        self.assertIsNotNone(plot.plant)
        self.assertEqual(plot.plant.id, plant.id)
        self.assertEqual(plot.remaining, plant.base_time)

    def test_plot_init_with_fertilizer_available_reduces_time(self):
        idx = 1
        plant = self.model.plants[0]  

        self.model.plots[idx].fertilizer_charges = 0
        self.model.plot_init(plant.id, idx, fertilizer_available=True)

        plot = self.model.plots[idx]
        self.assertEqual(plot.state, "growing")

        expected = int(plant.base_time * 0.8)
        self.assertEqual(plot.remaining, expected)

    def test_plot_init_uses_plot_fertilizer_charges_if_present(self):
        idx = 2
        plant = self.model.plants[1]  

        self.model.plots[idx].fertilizer_charges = 2
 
        self.model.plot_init(plant.id, idx, fertilizer_available=False)

        plot = self.model.plots[idx]
        self.assertEqual(plot.state, "growing")
        self.assertEqual(plot.remaining, int(plant.base_time * 0.8))

        self.assertEqual(plot.fertilizer_charges, 1)

    def test_harvest_increments_barn_and_resets_plot(self):
        idx = 3

        plant = Plant(99, "testcrop", 1000)
        plot = self.model.plots[idx]
        plot.state = "ready"
        plot.plant = plant
        plot.remaining = 0

        self.model.harvest(idx)
        self.assertIn("testcrop", self.model.barn)
        self.assertEqual(self.model.barn["testcrop"], 1)

        self.assertEqual(plot.state, "empty")
        self.assertIsNone(plot.plant)
        self.assertEqual(plot.remaining, 0)

        plot.plant = plant
        plot.state = "ready"
        self.model.harvest(idx)
        self.assertEqual(self.model.barn["testcrop"], 2)


if __name__ == "__main__":
    unittest.main()