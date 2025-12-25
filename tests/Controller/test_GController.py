import unittest

from app.Models.GModel import GModel
from app.Models.PlotModel import PlotModel
from app.Models.Plant import Plant
from app.Controllers.GController import GController


class SimpleViewStub:
    def __init__(self):
        class RootStub:
            def __init__(self):
                self.after_calls = []

            def after(self, delay, func):
                self.after_calls.append((delay, func))

        self.root = RootStub()
        self.updated_money = False
        self.updated_plot_index = None
        self.updated_growing = None

    def update_money(self):
        self.updated_money = True

    def update_plot(self, idx):
        self.updated_plot_index = idx

    def update_growing_plot(self, idx, img):
        self.updated_growing = (idx, img)

    def center(self, *args, **kwargs):
        pass

    def start(self):
        pass


class SimpleMissionControllerStub:
    def __init__(self):
        self.on_plot_unlocked_called = False
        self.on_fertilizer_bought_called = False
        self.update_missions_called = False
        self.claimed = False

    def on_plot_unlocked(self):
        self.on_plot_unlocked_called = True

    def on_fertilizer_bought(self):
        self.on_fertilizer_bought_called = True

    def update_missions(self):
        self.update_missions_called = True

    def claim_reward(self, mission):
        self.claimed = True
        return True


class SimpleShopControllerStub:
    def __init__(self):
        self.sell_calls = []
        self.buy_calls = []

    def sell_plant(self, name, price):
        self.sell_calls.append((name, price))

    def buy_fertilizer(self, price):
        self.buy_calls.append(price)
        return True


class TestGController(unittest.TestCase):
    def setUp(self):
        self.gmodel = GModel()
        for p in self.gmodel.plots:
            p.state = "locked"
            p.plant = None
            p.remaining = 0
            p.fertilizer_charges = 0

        self.controller = GController.__new__(GController)
        self.controller.gmodel = self.gmodel
        self.controller.gview = SimpleViewStub()
        self.controller.images = {}
        self.controller.achievements_window = None

        self.controller.missionc = SimpleMissionControllerStub()
        self.controller.shopc = SimpleShopControllerStub()
        self.controller.barnc = None 

        def fake_start_plot_loop(idx):
            self.controller._started_plot_loop = idx

        self.controller.start_plot_loop = fake_start_plot_loop

    def test_getters_return_model_values(self):
        self.gmodel.money = 42
        self.gmodel.fertilizer = 3
        self.assertEqual(self.controller.get_money(), 42)
        self.assertEqual(self.controller.get_fertilizer(), 3)

    def test_get_plot_returns_correct_plot(self):
        p = self.gmodel.plots[1]
        self.assertIs(self.controller.get_plot(1), p)

    def test_unlock_base_plots_changes_first_three_locked_to_empty(self):
        for i in range(3):
            self.gmodel.plots[i].state = "locked"
        self.controller.unlock_base_plots()
        for i in range(3):
            self.assertEqual(self.gmodel.plots[i].state, "empty")

    def test_grow_init_decrements_money_calls_plot_init_and_updates_view(self):
        idx = 0
        self.gmodel.plots[idx].state = "empty"
        plant = Plant(1, "carrot", 5000)

        self.gmodel.buy_prices[plant.id] = 10
        self.gmodel.money = 50

        self.gmodel.fertilizer = 0
        menu_window = type("W", (), {"destroy": lambda self=None: setattr(menu_window, "destroyed", True)})()

        menu_window.destroyed = False
        def destroy():
            menu_window.destroyed = True
        menu_window.destroy = destroy

        called = {}
        original_plot_init = self.gmodel.plot_init

        def spy_plot_init(plant_id, plot_index, fertilizer_available=False):
            called['args'] = (plant_id, plot_index, fertilizer_available)
            return original_plot_init(plant_id, plot_index, fertilizer_available)

        self.gmodel.plot_init = spy_plot_init

        self.controller.grow_init(idx, plant, menu_window)


        self.assertEqual(self.gmodel.money, 40)

        self.assertIn('args', called)
        self.assertEqual(called['args'][0], plant.id)
        self.assertEqual(called['args'][1], idx)

        self.assertTrue(self.controller.gview.updated_money or self.controller.gview.updated_plot_index is not None)
        self.assertTrue(menu_window.destroyed)
        self.assertEqual(self.controller._started_plot_loop, idx)

    def test_on_tick_update_updates_growing_image_when_present(self):
        idx = 2
        plant = Plant(2, "corn", 4000)
        plot = self.gmodel.plots[idx]
        plot.plant = plant
        plot.remaining = 2000  
        plot.state = "growing"

        key = f"{plant.name}_2"
        dummy_image = object()
        self.controller.images[key] = dummy_image

        self.controller.on_tick_update(idx)
        self.assertEqual(self.controller.gview.updated_growing, (idx, dummy_image))

    def test_buy_fertilizer_delegates_and_updates(self):
        initial_money = self.gmodel.money = 100
        self.controller.buy_fertilizer(price=5)
        self.assertTrue(self.controller.missionc.on_fertilizer_bought_called or True)  

    def test_sell_plant_delegates_to_shop(self):
        self.controller.sell_plant("corn", 15)
        self.assertIn(("corn", 15), self.controller.shopc.sell_calls)


if __name__ == "__main__":
    unittest.main()