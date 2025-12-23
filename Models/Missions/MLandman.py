from Models.Mission import Mission

class MLandman(Mission):
    def __init__(self):
        super().__init__(mission_id=3, name="Landman", description="Unlock all plots.", reward_gold=600)
        self.unlocked = 0

    def on_plot_unlocked(self, amount=1):
        if self.completed:
            return
        self.unlocked += amount
        if self.unlocked >= 2:
            self.completed = True

    def check(self, game_state) -> bool:
        return self.completed