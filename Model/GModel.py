class Plant:
    def __init__(self, pid, name, base_time):
        self.id = pid
        self.name = name
        self.base_time = base_time

class GModel:
    def __init__(self):
        self.money = 50
        self.fertilizer = 0
        self.sell_prices = {
            1: 15,
            2: 30,
            3: 60,
        }
        self.plants = [
            Plant(1, "carrot", 5000),
            Plant(2, "corn", 4000),
            Plant(3, "wheat", 9000),
        ]
        self.barn = {}

    def grow(btn_name, grow_pos):
        pass

    def harvest(btn_name, harvest_pos):
        pass

    def start_thread(btn_name, start_pos):
        pass

class PlotModel:
    def __init__(self, index):
        self.index = index
        self.state = "empty"
        self.plant = None
        self.remaining = 0
        self.timer_id = None

    def start_growth(self, plant: Plant):
        self.state = "growing"
        self.plant = plant
        if self.fertilizer > 0:
            self.fertilizer -= 1
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

