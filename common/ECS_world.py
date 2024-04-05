import os
import sys

if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.managers.entity_manager import EntityManager
from common.managers.event_manager import EventManager
from common.managers.input_manager import InputManager
from common.managers.system_manager import SystemManager

class ECSWorld:
    def __init__(self, game_state, logger, world_data = None):
        self.game_state = game_state
        self.logger = logger
        self.entity_manager = EntityManager(self.logger)
        self.event_manager = EventManager(self.logger)

        self.input_manager = InputManager(self.event_manager, self.logger)
        self.system_manager = SystemManager(self.game_state, self.entity_manager, self.event_manager, self.logger)

        if world_data:
            self.load_world_data(world_data)

    def load_world_data(self, world_data):
        self.entity_manager.create_world_entities(world_data["entities"])
        self.system_manager.add_systems(world_data["systems"])
        self.input_manager.load_input_data(world_data["input"])

def main():
    pass

if __name__ == "__main__":
    main()