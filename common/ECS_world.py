import os
import sys

if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.entity_manager import EntityManager
from common.event_manager import EventManager
from common.input_manager import InputManager
from common.system_manager import SystemManager

class ECSWorld:
    def __init__(self, game_state, world_data = None):
        self.game_state = game_state
        self.entity_manager = EntityManager(self)
        self.event_manager = EventManager(self)
        self.input_manager = InputManager(self)
        self.system_manager = SystemManager(self)

def main():
    pass

if __name__ == "__main__":
    main()