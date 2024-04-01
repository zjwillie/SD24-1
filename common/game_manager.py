import os
import sys

if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.components import *

from common.ECS_world import ECSWorld
from common.game_state import GameState

from core.logging_manager import LoggingManager
from core.utils import get_JSON_data

class GameManager:
    def __init__(self):

        self.game_state = GameState()
        self.world = None

        self.logger = LoggingManager()
        self.logger.initialize_logging()
        self.logger.set_output_to_console('game_manager')
        self.logger.change_log_level('game_manager', "INFO")

    def intialize_game(self):
        main_menu_dict = get_JSON_data("world/main_menu_world.json")
        self.world = ECSWorld(self.game_state, self.logger, main_menu_dict)

        # Turn off the option menu and option selector
        options_menu = self.world.entity_manager.get_entity_by_name("options_menu_background")
        self.world.entity_manager.entities_to_render.remove(options_menu)

        options_selector = self.world.entity_manager.get_entity_by_name("options_menu_selector")
        self.world.entity_manager.entities_to_render.remove(options_selector)
        self.world.entity_manager.menu_entities.remove(options_selector)


        self.world.event_manager.subscribe("escape", self.quit_game)
        self.world.event_manager.subscribe("change_state", self.change_state)

    def test_initialize(self):
        test_world_dict = get_JSON_data("common/test_world.json")
        self.world = ECSWorld(self.game_state, self.logger, test_world_dict)
        
        """
        test_dict = {
            "NameComponent": {
                "name": "Player 2"
            },
            "UUIDComponent": {}
        }
        self.world.entity_manager.create_entity_from_dict(test_dict)

        test_json = "common/test_json_entity.json"
        self.world.entity_manager.create_entity_from_JSON(test_json)

        self.world.entity_manager.create_world_entities(test_world_json)
        """
        
        self.world.event_manager.subscribe("escape", self.quit_game)
        self.world.event_manager.subscribe("change_state", self.change_state)

    def change_state(self, event):
        self.logger.loggers['game_manager'].info(f"Changing State to: {event.data}")
        if event.data == "quit":
            self.quit_game(event)

        elif event.data == "options":
            print("options")
            # Turn on the option menu and option selector
            options_menu = self.world.entity_manager.get_entity_by_name("options_menu_background")
            self.world.entity_manager.entities_to_render.add(options_menu)

            options_selector = self.world.entity_manager.get_entity_by_name("options_menu_selector")
            self.world.entity_manager.entities_to_render.add(options_selector)
            self.world.entity_manager.menu_entities.add(options_selector)
            self.world.entity_manager.get_component(options_selector, MenuSelectorComponent).current_selection = 0

            # Turn off the main menu and main menu selector
            main_menu = self.world.entity_manager.get_entity_by_name("main_menu_background")
            self.world.entity_manager.entities_to_render.remove(main_menu)

            main_selector = self.world.entity_manager.get_entity_by_name("main_menu_selector")
            self.world.entity_manager.entities_to_render.remove(main_selector)
            self.world.entity_manager.menu_entities.remove(main_selector)


        elif event.data == "main_menu":
            print("main_menu")
            # Turn on the main menu and main menu selector
            main_menu = self.world.entity_manager.get_entity_by_name("main_menu_background")
            self.world.entity_manager.entities_to_render.add(main_menu)

            main_selector = self.world.entity_manager.get_entity_by_name("main_menu_selector")
            self.world.entity_manager.entities_to_render.add(main_selector)
            self.world.entity_manager.menu_entities.add(main_selector)
            self.world.entity_manager.get_component(main_selector, MenuSelectorComponent).current_selection = 0

            # Turn off the option menu and option selector
            options_menu = self.world.entity_manager.get_entity_by_name("options_menu_background")
            self.world.entity_manager.entities_to_render.remove(options_menu)

            options_selector = self.world.entity_manager.get_entity_by_name("options_menu_selector")
            self.world.entity_manager.entities_to_render.remove(options_selector)
            self.world.entity_manager.menu_entities.remove(options_selector)


    def quit_game(self, event):
        self.logger.loggers['game_manager'].info("Quitting Game")
        self.game_state.exit_requested = True

    def update(self, delta_time):
        self.world.input_manager.update(delta_time)
        self.world.event_manager.update()
        self.world.system_manager.update(delta_time)

def main():

    game_manager = GameManager()

    game_manager.test_initialize()
    
    for entity in game_manager.world.entity_manager.entities:
        game_manager.logger.loggers['game_manager'].debug(f"Entity: {entity}")
        game_manager.logger.loggers['game_manager'].warning(f"{game_manager.world.entity_manager.get_component(entity, NameComponent).name}")
        game_manager.logger.loggers['game_manager'].critical(f"{game_manager.world.entity_manager.get_component(entity, UUIDComponent).uuid}")

    
if __name__ == "__main__":
    from common.components import *
    main()