from Models.Mission import Mission

class MFertilizerCollector(Mission):
    def __init__(self):
        super().__init__(mission_id=2, name="Fertilizer Collector", description="Buy 10 fertilizers.", reward_gold=100)
        self.bought = 0

    def on_fertilizer_bought(self, amount=1):
        if self.completed:
            return
        self.bought += amount
        if self.bought >= 10:
            self.completed = True

    def check(self, game_state) -> bool:
        return self.completed