from abc import ABC, abstractmethod

class Mission(ABC):
    def __init__(self, mission_id, name, description, reward_gold):
        self.mission_id = mission_id
        self.name = name
        self.description = description
        self.reward_gold = reward_gold
        self.reward_given = False
        self.completed = False

    @abstractmethod
    def check(self, game_state) -> bool:
        pass