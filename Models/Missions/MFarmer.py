from Models.Mission import Mission

class MFarmer(Mission):
    def __init__(self):
        super().__init__(mission_id=4, name="Plant Collector", description="Collect at least 10 of each plant.", reward_gold=400)
        self.collected = {}  

    def on_plant_collected(self, plant_name, amount=1):
        if self.completed:
            return
        # Only track known plants
        if plant_name in ["carrot", "corn", "wheat"]:
            self.collected[plant_name] = self.collected.get(plant_name, 0) + amount
        # Check that each required plant reached 10
        if all(self.collected.get(p, 0) >= 10 for p in ["carrot", "corn", "wheat"]):
            self.completed = True

    def check(self, game_state) -> bool:
        return self.completed