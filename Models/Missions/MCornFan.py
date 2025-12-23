from Models.Mission import Mission

class MCornFan(Mission):
    def __init__(self):
        super().__init__(mission_id=1, name="Corn Fan", description="Collect 30 corns.", reward_gold=150)
        self.collected = 0

    def on_plant_collected(self, plant_name, amount=1):
        if self.completed:
            return
        self.collected += amount
        if self.collected >= 30:
            self.completed = True

    def check(self, game_state) -> bool:
        return self.completed