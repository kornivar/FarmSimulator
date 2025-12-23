from Models.Mission import Mission

class MFarmer(Mission):
    def __init__(self):
        super().__init__(mission_id=4, name="Plant Collector", description="Collect at least 10 of each plant.", reward_gold=400)
        self.collected = {}  # ключ = название растени€, значение = количество

    def on_plant_collected(self, plant_name, amount=1):
        if self.completed:
            return
        self.collected[plant_name] = self.collected.get(plant_name, 0) + amount
        if all(v >= 10 for v in self.collected.values()):
            self.completed = True

    def check(self, game_state) -> bool:
        return self.completed