from ..Mission import Mission

class MWhatsUpDoc(Mission):
	def __init__(self):
		super().__init__(mission_id=0, name="What's up, Doc?", description="Collect 50 carrots.", reward_gold=200)
		self.collected = 0

	def on_plant_collected(self, plant_name, amount=1):
		if self.completed:
			return
		# Count only carrots
		if plant_name == "carrot":
			self.collected += amount
			if self.collected >= 50:
				self.completed = True

	def check(self, game_state) -> bool:
		return self.completed