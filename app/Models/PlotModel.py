from .Plant import Plant

class PlotModel:
    def __init__(self, index):
        self.index = index
        self.state = "locked"
        self.plant = None
        self.remaining = 0

        self.plot_type = "basic"
        self.fertilizer_charges = 0

    @property
    def fertilizer(self):
        return self.fertilizer_charges

    @fertilizer.setter
    def fertilizer(self, value):
        self.fertilizer_charges = value

    def unlock(self):
        if self.state == "locked":
            self.state = "empty"

    def start_growth(self, plant: Plant, fertilizer_available=False):
        self.state = "growing"
        self.plant = plant

        if self.fertilizer_charges > 0:
            self.fertilizer_charges -= 1
            self.remaining = int(plant.base_time * 0.8)
        else:
            if fertilizer_available:
                self.remaining = int(plant.base_time * 0.8) 
            else:
                self.remaining = plant.base_time

    def tick(self, callback):
        if self.remaining <= 0:
            self.state = "ready"
            callback("finish")
            return

        self.state = "growing"

        self.remaining -= 1000
        callback("tick")

