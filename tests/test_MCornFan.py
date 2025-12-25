import unittest
from app.Models.Missions.MCornFan import MCornFan

class TestCornFanMission(unittest.TestCase):

    def test_mission_completes_after_30_corn(self):
        mission = MCornFan()
        for _ in range(30):
            mission.on_plant_collected("corn")
        self.assertTrue(mission.completed)

    def test_other_plants_do_not_count(self):
        mission = MCornFan()
        mission.on_plant_collected("carrot", 30)
        self.assertFalse(mission.completed)

if __name__ == "__main__":
    unittest.main()