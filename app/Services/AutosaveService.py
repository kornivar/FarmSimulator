import json
import os

class AutosaveService:

    def __init__(self, gmodel):
        self.gmodel = gmodel
        self.program_autosave = "app/program_autosave.json"
        self.data = {}

    def save_game(self):
        plots  =   [              
            {
                    "state": plot.state,
                    "plant_id": plot.plant.id if plot.plant else None,
                    "remaining": plot.remaining,
                    "plot_type": plot.plot_type,
                    "super_fertilizer": plot.fertilizer_charges,
            } for plot in self.gmodel.plots
        ]
        missions = [
            {
                "mission_id": mission.mission_id,
                "completed": mission.completed,
                "reward_given": mission.reward_given,
                "collected": getattr(mission, 'collected', 0),
            } for mission in self.gmodel.missions.values()
        ]

        self.data = {
            "money": self.gmodel.money,
            "fertilizer": self.gmodel.fertilizer,
            "barn": self.gmodel.barn,
            "plots": plots,
            "missions": missions,
        }

        with open(self.program_autosave, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4)

    def load_game(self):
        if not os.path.exists(self.program_autosave):
            return
        try:
            with open(self.program_autosave, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
        except:
            return

        loaded_data = save_data

        self.gmodel.money = loaded_data.get("money", 0)
        self.gmodel.fertilizer = loaded_data.get("fertilizer", 0)
        self.gmodel.barn = loaded_data.get("barn", {})

        plots_data = loaded_data.get("plots", [])

        for i, plot_data in enumerate(plots_data):
            if i >= len(self.gmodel.plots):
                break
            plot = self.gmodel.plots[i]
            plot.state = plot_data.get("state", "locked")
            plant_id = plot_data.get("plant_id")
            if plant_id is not None:
                plant = next((p for p in self.gmodel.plants if p.id == plant_id), None)
                plot.plant = plant
            else:
                plot.plant = None
            plot.remaining = plot_data.get("remaining", 0)
            plot.plot_type = plot_data.get("plot_type", "basic")
            plot.fertilizer_charges = plot_data.get("super_fertilizer", 0)

        for mission_data in loaded_data.get("missions", []):
            mission_id = mission_data.get("mission_id")
            mission = self.gmodel.missions.get(mission_id)
            if mission:
                mission.completed = mission_data.get("completed", False)
                mission.reward_given = mission_data.get("reward_given", False)
                if hasattr(mission, 'collected'):
                    mission.collected = mission_data.get("collected", 0)

