import os
import sys

if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.components import *

from common.event_manager import Event

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
        options_menu = self.world.entity_manager.get_entity_by_name(self.world.event_manager.OPTIONS_MENU_BACKGROUND)
        self.world.entity_manager.entities_to_render.remove(options_menu)

        options_selector = self.world.entity_manager.get_entity_by_name(self.world.event_manager.OPTIONS_MENU_SELECTOR)
        self.world.entity_manager.entities_to_render.remove(options_selector)
        self.world.entity_manager.menu_entities.remove(options_selector)

        self.world.event_manager.subscribe(self.world.event_manager.EVENT_ESCAPE, self.quit_game)
        self.world.event_manager.subscribe(self.world.event_manager.CHANGE_STATE, self.change_state)
        
        #TODO this should be in world data
        #self.world.event_manager.post(Event(self.world.event_manager.TIME_BETWEEN_REPEATS, 0.2))

        self.world.event_manager.post(Event(self.world.event_manager.SET_MENU, (self.world.event_manager.MAIN_MENU_BACKGROUND, self.world.event_manager.MAIN_MENU_SELECTOR, True)))


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
        self.logger.loggers['game_manager'].info(f"Changing State to: {event.data[0]}")
        if event.data[0] == self.world.event_manager.QUIT:
            self.quit_game(event)

        elif event.data[0] == self.world.event_manager.OPTIONS:
            if self.world.game_state.sound_on:
                self.world.event_manager.post(Event(self.world.event_manager.SET_MENU, (self.world.event_manager.OPTIONS_MENU_BACKGROUND, self.world.event_manager.OPTIONS_MENU_SELECTOR, event.data[1])))
            else:
                self.world.event_manager.post(Event(self.world.event_manager.SET_MENU, (self.world.event_manager.OPTIONS_MENU_BACKGROUND_NO_SOUND, self.world.event_manager.OPTIONS_MENU_SELECTOR, event.data[1])))

        elif event.data[0] == self.world.event_manager.MAIN_MENU:
            self.world.event_manager.post(Event(self.world.event_manager.SET_MENU, (self.world.event_manager.MAIN_MENU_BACKGROUND, self.world.event_manager.MAIN_MENU_SELECTOR, event.data[1])))

        elif event.data[0] == self.world.event_manager.SOUND:
            self.world.game_state.sound_on = not self.world.game_state.sound_on
            # Need to pass False so the selector doesn't reset
            self.world.event_manager.post(Event(self.world.event_manager.CHANGE_STATE, (self.world.event_manager.OPTIONS, False)))


    def quit_game(self, event):
        self.logger.loggers['game_manager'].info("Quitting Game")
        self.game_state.exit_requested = True

    def update(self, delta_time):
        self.world.input_manager.update()
        self.world.event_manager.update()
        self.world.system_manager.update(delta_time)
        #self.logger.loggers["game_manager"].info(f"Keys that are down: {self.world.input_manager.keys_down}")

####################################################################################################

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