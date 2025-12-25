from ..Mission import Mission

class MLandman(Mission):
    def __init__(self):
        super().__init__(mission_id=3, name="Landman", description="Unlock all plots.", reward_gold=400)
        self.unlocked = 0

    def on_plot_unlocked(self, amount=1):
        if self.completed:
            return
        self.unlocked += amount
        # require unlocking 2 additional plots (total unlocked >= 5 triggers completion)
        if self.unlocked >= 2:
            self.completed = True

    def check(self, game_state) -> bool:
        # Alternatively, verify by checking actual game state unlocked plots
        unlocked = sum(1 for p in game_state.plots if p.state != "locked")
        return unlocked >= 5 or self.completed
