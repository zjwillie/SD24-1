import os
import sys

if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
                    
from common.ECS_world import ECSWorld
from common.entity_manager import EntityManager
from common.event_manager import EventManager
from common.input_manager import InputManager
from common.system_manager import SystemManager
from common.ECS_world import ECSWorld

from common.game_state import GameState

class GameManager:
    def __init__(self):

        self.game_state = GameState()


    def initialize(self):
        pass

def main():
    game_manager = GameManager()
    
if __name__ == "__main__":
    main()