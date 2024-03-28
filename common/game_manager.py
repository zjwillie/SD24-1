import os
import sys

if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.components import NameComponent, UUIDComponent
                    
from common.ECS_world import ECSWorld
from common.game_state import GameState

class GameManager:
    def __init__(self):

        self.game_state = GameState()
        self.world = ECSWorld(self.game_state)

        self.initialize()

    def initialize(self):
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


def main():
    game_manager = GameManager()
    
    for entity in game_manager.world.entity_manager.entities:
        print(entity)
        print(game_manager.world.entity_manager.get_component(entity, NameComponent).name)
        print(game_manager.world.entity_manager.get_component(entity, UUIDComponent).uuid)

    
if __name__ == "__main__":
    main()