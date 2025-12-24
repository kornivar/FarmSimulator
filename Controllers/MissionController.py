from Models.Missions.MWhatsUpDoc import MWhatsUpDoc
import logging
logger = logging.getLogger(__name__)

class MissionController:
    def __init__(self, gmodel):
        self.gmodel = gmodel

    def on_plant_collected(self, plant_name: str, amount: int = 1):
        logger.info(f"Plant collected: {plant_name} x{amount}, notifying missions...")
        for mission in self.gmodel.missions.values():
            if hasattr(mission, "on_plant_collected"):
                try:
                    mission.on_plant_collected(plant_name, amount)
                except Exception as e:
                    # ignore missions that don't expect this plant or have other issues
                    logger.error(f"Error in mission '{mission.name}' on_plant_collected: {e}")
                    pass

    def on_plot_unlocked(self):
        logger.info("Plot unlocked, notifying missions...")
        for mission in self.gmodel.missions.values():
            if hasattr(mission, "on_plot_unlocked"):
                try:
                    mission.on_plot_unlocked()
                except Exception as e:
                    logger.error(f"Error in mission '{mission.name}' on_plot_unlocked: {e}")
                    pass

    def on_fertilizer_bought(self):
        logger.info("Fertilizer bought, notifying missions...")
        for mission in self.gmodel.missions.values():
            if hasattr(mission, "on_fertilizer_bought"):
                try:
                    mission.on_fertilizer_bought()
                except Exception as e:
                    logger.error(f"Error in mission '{mission.name}' on_fertilizer_bought: {e}")
                    pass


    def update_missions(self):
        logger.info("Updating mission statuses...")
        for mission in self.gmodel.missions.values():
            try:
                if mission.check(self.gmodel):
                    mission.completed = True
            except Exception as e:
                logger.error(f"Error updating mission '{mission.name}': {e}")
                pass

    def claim_reward(self, mission):
        logger.info(f"Claiming reward for mission '{mission.name}'...")
        # Grant reward only when user explicitly claims
        if mission.completed and not mission.reward_given:
            self.gmodel.money += mission.reward_gold
            mission.reward_given = True
            print(f"Mission '{mission.name}' reward claimed: {mission.reward_gold} gold.")
            return True
        return False