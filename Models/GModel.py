from Models.Plant import Plant
from Models.PlotModel import PlotModel
import json
import os 

user_safe = "save.txt"
program_data = "program_data.json"

class GModel:
    def __init__(self):
        self.money = 50
        self.fertilizer = 0
        self.sell_prices = {
            1: 15,
            2: 30,
            3: 60,
        }
        self.buy_prices = {
            1: 10,
            2: 20,
            3: 40,
        }
        self.plants = [
            Plant(1, "carrot", 5000),
            Plant(2, "corn", 4000),
            Plant(3, "wheat", 9000),
        ]
        self.barn = {}
        self.plots = [PlotModel(i) for i in range(5)]

    def harvest(self, plot_index):
        plot = self.plots[plot_index]
        name = plot.plant.name

        self.barn[name] = self.barn.get(name, 0) + 1
        plot.state = "empty"
        plot.plant = None
        plot.remaining = 0

    def start_thread(self, plant_id, plot_index, fertilizer_available=False):
        plot = self.plots[plot_index]
        plant = next(p for p in self.plants if p.id == plant_id)
        plot.start_growth(plant, fertilizer_available)

    def save_game(self):
        lines=[]
        lines.append(f"money={self.money}")

        barn_str=",".join([f"{name}:{count}" for name, count in self.barn.items()])
        lines.append(f"barn={barn_str}")

        lines.append(f"fertilizer={self.fertilizer}")

        with open(user_safe, "w") as f:
            f.write("\n".join(lines))

    def load_game(self):
        if not os.path.exists(user_safe):
            return
        try:
            with open(user_safe, "r") as f:
                lines = f.read().splitlines()
        except:
            return

        data={}

        for line in lines:
            if "=" in line:
                key, value = line.split("=", 1)
                data[key] = value

        self.money = int(data.get("money", 0))

        barn_raw = data.get("barn", "")
        self.barn = {}
        if barn_raw:
            for item in barn_raw.split(","):
                if ":" in item:
                    name, count = item.split(":")
                    self.barn[name] = int(count)

        self.fertilizer = int(data.get("fertilizer", 0))


