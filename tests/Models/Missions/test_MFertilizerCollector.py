import unittest
from app.Models.Missions.MFertilizerCollector import MFertilizerCollector

class TestFertilizerCollectorMission(unittest.TestCase):

    def test_mission_completes_after_collecting_10_fertilizer(self):
        mission = MFertilizerCollector()
        for _ in range(10):
            mission.on_fertilizer_bought(1)
        self.assertTrue(mission.completed)

    def test_partial_collection_does_not_complete_mission(self):
        mission = MFertilizerCollector()
        for _ in range(9):
            mission.on_fertilizer_bought(1)
        self.assertFalse(mission.completed)

if __name__ == "__main__":
    unittest.main()