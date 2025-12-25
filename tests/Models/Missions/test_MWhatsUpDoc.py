import unittest
from app.Models.Missions.MWhatsUpDoc import MWhatsUpDoc

class TestWhatsUpDocMission(unittest.TestCase):

    def test_mission_completes_after_50_carrots(self):
        mission = MWhatsUpDoc()
        for _ in range(50):
            mission.on_plant_collected("carrot")
        self.assertTrue(mission.completed)

    def test_other_plants_do_not_count(self):
        mission = MWhatsUpDoc()
        mission.on_plant_collected("wheat", 50)
        self.assertFalse(mission.completed)

if __name__ == "__main__":
    unittest.main()

