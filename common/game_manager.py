import os
import sys

if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.components import NameComponent, UUIDComponent
                    
from common.ECS_world import ECSWorld
from common.game_state import GameState

from core.logging_manager import LoggingManager

class GameManager:
    def __init__(self):

        self.game_state = GameState()
        self.world = None

        self.logger = LoggingManager()
        self.logger.initialize_logging()
        self.logger.set_output_to_console('game_manager')
        self.logger.change_log_level('game_manager', "DEBUG")


    def test_initialize(self):

        self.world = ECSWorld(self.game_state, self.logger)

        test_dict = {
            "NameComponent": {
                "name": "Player 2"
            },
            "UUIDComponent": {}
        }
        self.world.entity_manager.create_entity_from_dict(test_dict)

        test_json = "common/test_json_entity.json"
        self.world.entity_manager.create_entity_from_JSON(test_json)

        test_world_json = "common/test_world.json"
        self.world.entity_manager.create_world_entities(test_world_json)

        self.world.event_manager.subscribe("escape", self.quit_game)

    def quit_game(self, event):
        self.logger.loggers['game_manager'].info("Quitting Game")
        self.game_state.exit_requested = True


    def update(self, delta_time):
        self.world.event_manager.update()
        self.world.input_manager.update(delta_time)

def main():
    game_manager = GameManager()

    game_manager.test_initialize()
    
    for entity in game_manager.world.entity_manager.entities:
        game_manager.logger.loggers['game_manager'].debug(f"Entity: {entity}")
        game_manager.logger.loggers['game_manager'].warning(f"{game_manager.world.entity_manager.get_component(entity, NameComponent).name}")
        game_manager.logger.loggers['game_manager'].critical(f"{game_manager.world.entity_manager.get_component(entity, UUIDComponent).uuid}")

    
if __name__ == "__main__":
    main()