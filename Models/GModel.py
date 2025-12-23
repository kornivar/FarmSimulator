from Models.Plant import Plant
from Models.PlotModel import PlotModel
from Models.Missions.MWhatsUpDoc import MWhatsUpDoc
import logging
logger = logging.getLogger(__name__)

class GModel:
    def __init__(self):
        logger.info("Initializing Game Model...")
        self.money = 700
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

        self.missions = {
            0: MWhatsUpDoc(),
        }

        self.barn = {}
        self.plots = [PlotModel(i) for i in range(5)]

    def harvest(self, plot_index):
        logger.info(f"Harvesting plot at index {plot_index}...")
        plot = self.plots[plot_index]
        name = plot.plant.name

        self.barn[name] = self.barn.get(name, 0) + 1
        plot.state = "empty"
        plot.plant = None
        plot.remaining = 0

    def plot_init(self, plant_id, plot_index, fertilizer_available=False):
        logger.info(f"Initializing plot at index {plot_index} with plant ID {plant_id}...")
        plot = self.plots[plot_index]
        plant = next(p for p in self.plants if p.id == plant_id)
        plot.start_growth(plant, fertilizer_available)


