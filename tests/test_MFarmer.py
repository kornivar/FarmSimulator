import unittest
from app.Models.Missions.MFarmer import MFarmer

class TestFarmerMission(unittest.TestCase):

    def test_mission_completes_after_collecting_10_of_each_plant(self):
        mission = MFarmer()
        for _ in range(10):
            mission.on_plant_collected("carrot")
            mission.on_plant_collected("corn")
            mission.on_plant_collected("wheat")
        self.assertTrue(mission.completed)

    def test_partial_collection_does_not_complete_mission(self):
        mission = MFarmer()
        for _ in range(10):
            mission.on_plant_collected("carrot")
            mission.on_plant_collected("corn")
        for _ in range(9):
            mission.on_plant_collected("wheat")
        self.assertFalse(mission.completed)

if __name__ == "__main__":
    unittest.main()