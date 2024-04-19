
from common.systems.animation_system import AnimationSystem
from common.systems.camera_system import CameraSystem
from common.systems.grid_system import GridSystem
from common.systems.dialogue_system import DialogueSystem
from common.systems.player_system import PlayerSystem
from common.systems.menu_system import MenuSystem
from common.systems.movement_system import MovementSystem
from common.systems.render_system import RenderSystem
from common.systems.time_system import TimeSystem
from common.systems.testing_system import TestingSystem

class SystemFactory:
    def __init__(self):
        self.system_classes = {
            'AnimationSystem': AnimationSystem,
            'CameraSystem': CameraSystem,
            'DialogueSystem': DialogueSystem,
            'GridSystem': GridSystem,
            'PlayerSystem': PlayerSystem,
            'MenuSystem': MenuSystem,
            'MovementSystem': MovementSystem,
            'RenderSystem': RenderSystem,
            'TimeSystem': TimeSystem,
            'TestingSystem': TestingSystem
        }

    def create_system(self, system_name, game_state, entity_manager, event_manager, logger):
        system_data = {
            'game_state': game_state,
            'entity_manager': entity_manager,
            'event_manager': event_manager,
            'logger': logger
        }
        system_class = self.system_classes.get(system_name)
        if system_class:
            try:
                return system_class(**system_data)
            except ValueError:
                print(f"Error: Factory method for {system_name} not found. Skipping this system.")
                return None
        else:
            print(f"Error: Factory method for {system_name} not found. Skipping this system.")
            return None