import json
import os

class AutosaveService:

    def __init__(self, gmodel):
        self.gmodel = gmodel
        self.program_autosave = "program_autosave.json"
        self.data = {}

    def print(self):
        json_string = json.dumps(self.data, indent=4)
        print("JSON String:")
        print(json_string)

    def save_game(self):

        self.data = {
            "money": self.gmodel.money,
            "fertilizer": self.gmodel.fertilizer,
            "barn": self.gmodel.barn
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