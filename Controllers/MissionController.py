from Models.Missions.MWhatsUpDoc import MWhatsUpDoc

class MissionController:
    def __init__(self, gmodel):
        self.gmodel = gmodel

    def on_harvest(self, plant_name: str):
        if plant_name == "carrot":
            self.gmodel.missions[0].on_carrot_collected()

    def update(self):
        for mission in self.gmodel.missions.values():
            if mission.check(self.gmodel) and not mission.reward_given:
                self.gmodel.money += mission.reward_gold
                mission.reward_given = True