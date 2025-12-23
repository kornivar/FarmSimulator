from Models.Missions.MWhatsUpDoc import MWhatsUpDoc

class MissionController:
    def __init__(self, gmodel):
        self.gmodel = gmodel

    def on_plant_collected(self, plant_name: str, amount: int = 1):
        for mission in self.gmodel.missions:
            if hasattr(mission, "on_plant_collected"):
                mission.on_plant_collected(plant_name, amount)

    def on_plot_unlocked(self):
        for mission in self.gmodel.missions:
            if hasattr(mission, "on_plot_unlocked"):
                mission.on_plot_unlocked()

    def on_fertilizer_bought(self):
        for mission in self.gmodel.missions:
            if hasattr(mission, "on_fertilizer_bought"):
                mission.on_fertilizer_bought()



    def update_missions(self):
        for mission in self.gmodel.missions:
            if mission.check(self.gmodel) and not mission.reward_given:
                self.gmodel.money += mission.reward_gold
                mission.reward_given = True
                print(f"Mission '{mission.name}' completed! Reward: {mission.reward_gold} gold.")