import unittest

from app.Models.PlotModel import PlotModel
from app.Models.Plant import Plant


class TestPlotModel(unittest.TestCase):
    def setUp(self):
        self.plant_carrot = Plant(1, "carrot", 5000)
        self.plant_corn = Plant(2, "corn", 4000)

    def test_unlock_transitions_locked_to_empty_only_when_locked(self):
        plot = PlotModel(0)
        self.assertEqual(plot.state, "locked")
        plot.unlock()
        self.assertEqual(plot.state, "empty")

        plot.state = "empty"
        plot.unlock()
        self.assertEqual(plot.state, "empty")

    def test_start_growth_sets_state_and_plant_and_full_duration_when_no_fertilizer(self):
        plot = PlotModel(1)
        plot.fertilizer_charges = 0
        plot.start_growth(self.plant_carrot, fertilizer_available=False)

        self.assertEqual(plot.state, "growing")
        self.assertIsNotNone(plot.plant)
        self.assertEqual(plot.plant.id, self.plant_carrot.id)
        self.assertEqual(plot.remaining, self.plant_carrot.base_time)

    def test_start_growth_uses_fertilizer_available_flag_to_reduce_time(self):
        plot = PlotModel(2)
        plot.fertilizer_charges = 0
        plot.start_growth(self.plant_carrot, fertilizer_available=True)

        expected = int(self.plant_carrot.base_time * 0.8)
        self.assertEqual(plot.remaining, expected)

    def test_start_growth_prefers_plot_fertilizer_charges_and_decrements_them(self):
        plot = PlotModel(3)
        plot.fertilizer_charges = 2
        plot.start_growth(self.plant_corn, fertilizer_available=False)

        expected = int(self.plant_corn.base_time * 0.8)
        self.assertEqual(plot.remaining, expected)
        self.assertEqual(plot.fertilizer_charges, 1)

    def test_tick_with_zero_or_negative_remaining_calls_finish_and_sets_ready(self):
        plot = PlotModel(4)
        plot.remaining = 0
        called = []

        def cb(arg):
            called.append(arg)

        plot.tick(cb)

        self.assertEqual(plot.state, "ready")
        self.assertEqual(called, ["finish"])

        plot2 = PlotModel(5)
        plot2.remaining = -100
        called2 = []
        plot2.tick(lambda a: called2.append(a))
        self.assertEqual(plot2.state, "ready")
        self.assertEqual(called2, ["finish"])

    def test_tick_with_positive_remaining_decrements_and_calls_tick_then_finish_on_next_tick(self):
        plot = PlotModel(6)
        plot.remaining = 1500  

        events = []

        def cb(e):
            events.append(e)

        plot.tick(cb)
        self.assertEqual(events[-1], "tick")
        self.assertEqual(plot.remaining, 500)
        self.assertEqual(plot.state, "growing")

        plot.tick(cb)
        self.assertEqual(events[-1], "tick")

        plot.tick(cb)
        self.assertIn("finish", events)
        self.assertEqual(plot.state, "ready")

    def test_tick_with_exactly_one_second_decrements_to_negative_then_finish_on_next_tick(self):
        plot = PlotModel(7)
        plot.remaining = 1000

        events = []
        plot.tick(lambda e: events.append(e))
        self.assertEqual(events[-1], "tick")

        plot.tick(lambda e: events.append(e))
        self.assertEqual(events[-1], "finish")
        self.assertEqual(plot.state, "ready")


if __name__ == "__main__":
    unittest.main()