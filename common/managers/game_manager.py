import os
import sys

from pygame.math import Vector2

if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.components import *

from common.managers.event_manager import Event

from common.ECS_world import ECSWorld
from common.game_state import GameState

from common.managers.logging_manager import LoggingManager
from support.utils import get_JSON_data

class GameManager:
    def __init__(self):

        self.game_state = GameState()
        self.world = None

        self.logger = LoggingManager()
        log_levels = {
            'animation_system': "OFF",
            'camera_system': "OFF",
            'component': 'OFF',
            'current': 'OFF',
            'dialogue_system': "OFF",
            'entity_manager': 'OFF',
            'event_manager': 'OFF',
            'game_manager': 'OFF',
            'grid_system': 'ON',
            'input_manager': 'OFF',
            'menu_system': 'OFF',
            'movement_system': 'OFF',
            'player_system': 'OFF',
            'render_system': 'OFF',
            'system': 'OFF',
            'testing_system': 'OFF',
        }
        self.logger.set_log_levels(log_levels)
        #self.logger.set_output_to_console('game_manager')


    def intialize_game(self):
        self.load_main_menu()


    def change_state(self, event):
        self.logger.loggers['game_manager'].info(f"Changing State to: {event.data[0]}")
        if event.data[1]:
            self.logger.loggers['game_manager'].info(f"Selector: {event.data[1]}")

        if event.data[0] == self.world.event_manager.QUIT:
            self.quit_game(event)

        elif event.data[0] == self.world.event_manager.OPTIONS:
            self.change_menu(event)

        elif event.data[0] == self.world.event_manager.MAIN_MENU:
            self.load_main_menu()

        elif event.data[0] == self.world.event_manager.SOUND:
            self.toggle_sound(event)

        elif event.data[0] == self.world.event_manager.START_GAME:
            self.start_game()


    def change_menu(self, event):
        # Event data[1] is the selector, postion, if it's True, it is reset, if it's False, it is not and remains (this way we can toggle selections)
        if self.world.game_state.sound_on:
            self.world.event_manager.post(Event(self.world.event_manager.SET_MENU, (self.world.event_manager.OPTIONS_MENU_BACKGROUND, self.world.event_manager.OPTIONS_MENU_SELECTOR, event.data[1])))
        else:
            self.world.event_manager.post(Event(self.world.event_manager.SET_MENU, (self.world.event_manager.OPTIONS_MENU_BACKGROUND_NO_SOUND, self.world.event_manager.OPTIONS_MENU_SELECTOR, event.data[1])))


    def start_game(self):
        #start_game_dict = get_JSON_data("world/_testing_collision.json")
        start_game_dict = get_JSON_data("world/game_world.json")
        self.world = ECSWorld(self.game_state, self.logger, start_game_dict)

        world_size = self.game_state.world_size

        # Print all entities with their names:
        for entity in self.world.entity_manager.entities:
            self.logger.loggers['game_manager'].info(f"Entity: {entity}", end=" ")
            if self.world.entity_manager.has_component(entity, NameComponent):
                  self.logger.loggers['game_manager'].info(f"Name: {self.world.entity_manager.get_component(entity, NameComponent).name}")
        self.logger.loggers['game_manager'].info("END OF ENTITIES")        

        # Attach the camera to the player
        camera_data = get_JSON_data(start_game_dict["camera"])
        self.world.entity_manager.add_component(self.world.entity_manager.player_ID, 
                                                CameraComponent(
                                                    tuple(camera_data["position"]), 
                                                    tuple(camera_data["camera_size"]), 
                                                    tuple(world_size), 
                                                    tuple(camera_data["dead_zone"]),
                                                    tuple(camera_data["offset"])                                                    
                                                    )
                                                )
        
        self.world.entity_manager.get_component(self.world.entity_manager.player_ID, PositionComponent).position = Vector2(self.game_state.resolution[0] // 2, self.game_state.resolution[1] // 2)

        self.world.event_manager.subscribe(self.world.event_manager.QUIT, self.quit_game)
        self.world.event_manager.subscribe(self.world.event_manager.EVENT_ESCAPE, self.quit_game)
        self.world.event_manager.subscribe(self.world.event_manager.CHANGE_STATE, self.change_state)

    def load_main_menu(self):
        main_menu_dict = get_JSON_data("world/main_menu_world.json")
        self.world = ECSWorld(self.game_state, self.logger, main_menu_dict)

        self.world.event_manager.subscribe(self.world.event_manager.QUIT, self.quit_game)
        self.world.event_manager.subscribe(self.world.event_manager.EVENT_ESCAPE, self.quit_game)
        self.world.event_manager.subscribe(self.world.event_manager.CHANGE_STATE, self.change_state)

        self.world.event_manager.post(Event(self.world.event_manager.SET_MENU, (self.world.event_manager.MAIN_MENU_BACKGROUND, self.world.event_manager.MAIN_MENU_SELECTOR, True)))



    def quit_game(self, event):
        self.logger.loggers['game_manager'].info("Quitting Game")
        self.game_state.exit_requested = True

    def toggle_sound(self, event):
        self.world.game_state.sound_on = not self.world.game_state.sound_on
        # Need to pass False so the selector doesn't reset
        self.world.event_manager.post(Event(self.world.event_manager.CHANGE_STATE, (self.world.event_manager.OPTIONS, False)))

#?###########################################################################################
#? Update
#?###########################################################################################


    def update(self, delta_time):
        self.world.input_manager.update()
        self.world.event_manager.update()
        self.world.system_manager.update(delta_time)
        #self.logger.loggers["game_manager"].info(f"Keys that are down: {self.world.input_manager.keys_down}")



####################################################################################################

def main():
    pass

    """
    game_manager = GameManager()

    game_manager.test_initialize()
    
    for entity in game_manager.world.entity_manager.entities:
        game_manager.logger.loggers['game_manager'].debug(f"Entity: {entity}")
        game_manager.logger.loggers['game_manager'].warning(f"{game_manager.world.entity_manager.get_component(entity, NameComponent).name}")
        game_manager.logger.loggers['game_manager'].critical(f"{game_manager.world.entity_manager.get_component(entity, UUIDComponent).uuid}")
    """

if __name__ == "__main__":
    from common.components import *
    main()