import unittest
from app.Models.Missions.MLandman import MLandman

class TestLandmanMission(unittest.TestCase):

    def test_mission_completes_after_buying_2_plots(self):
        mission = MLandman()
        for _ in range(2):
            mission.on_plot_unlocked()
        self.assertTrue(mission.completed)

    def test_partial_purchase_does_not_complete_mission(self):
        mission = MLandman()
        for _ in range(1):
            mission.on_plot_unlocked()
        self.assertFalse(mission.completed)

    def test_check_method_with_game_state(self):
        class MockPlot:
            def __init__(self, state):
                self.state = state

        class MockGameState:
            def __init__(self, plots):
                self.plots = plots

        mission = MLandman()

        plots = [MockPlot("unlocked"), MockPlot("unlocked"), MockPlot("unlocked"), MockPlot("unlocked"), MockPlot("unlocked")]

        game_state = MockGameState(plots)
        self.assertTrue(mission.check(game_state))
        plots = [MockPlot("unlocked"), MockPlot("unlocked"), MockPlot("unlocked"), MockPlot("unlocked"), MockPlot("locked")]
        game_state = MockGameState(plots)
        self.assertFalse(mission.check(game_state))

if __name__ == "__main__":
    unittest.main()