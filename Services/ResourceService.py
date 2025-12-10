import json
import os

program_data = "program_data.json"

class ResourceService:
    resources = {}

    @staticmethod
    def init():
        if not os.path.exists(program_data):
            default_resources = {
                "carrot_0": "Resources/Images/carrot_1.png",
                "carrot_1": "Resources/Images/carrot_2.png",
                "carrot_2": "Resources/Images/carrot_3.png",
                "carrot_3": "Resources/Images/carrot_4.png",
                "corn_0": "Resources/Images/corn_1.png",
                "corn_1": "Resources/Images/corn_2.png",
                "corn_2": "Resources/Images/corn_3.png",
                "corn_3": "Resources/Images/corn_4.png",
                "wheat_0": "Resources/Images/wheat_1.png",
                "wheat_1": "Resources/Images/wheat_2.png",
                "wheat_2": "Resources/Images/wheat_3.png",
                "wheat_3": "Resources/Images/wheat_4.png",
            }
            try:
                with open(program_data, "w") as f:
                    json.dump(default_resources, f, indent=4)
            except Exception as e:
                print(f"Error creating JSON: {e}")

        try:
            with open(program_data, "r") as f:
                ResourceService.resources = json.load(f)
        except Exception as e:
            print(f"Error creating JSON: {e}")
            ResourceService.resources = {}

    @staticmethod
    def get_resource(key):
        return ResourceService.resources.get(key, None)
