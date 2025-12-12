from Models.Plant import Plant

class PlotModel:
    def __init__(self, index):
        self.index = index
        self.state = "locked"
        self.plant = None
        self.remaining = 0
        self.timer_id = None

    def start_growth(self, plant: Plant, fertilizer_available=False):
        self.state = "growing"
        self.plant = plant

        if fertilizer_available:
            self.remaining = int(plant.base_time * 0.8) 
        else:
            self.remaining = plant.base_time

    def tick(self, callback):
        if self.remaining <= 0:
            self.state = "ready"
            callback("finish")
            return

        self.remaining -= 1000
        callback("tick")

