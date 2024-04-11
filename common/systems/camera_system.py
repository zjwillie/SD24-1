# Camera System
from .base_system import System

class CameraSystem(System):
    def __init__(self, game_state, entity_manager, event_manager, logger):
        super().__init__(game_state, entity_manager, event_manager, logger)
        
        self.logger = logger.loggers['camera_system']

        self.camera_entity = None


    def update(self, delta_time):
        pass