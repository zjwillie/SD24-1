# Camera System
from .base_system import System

from common.managers.event_manager import Event

from common.components.camera_component import CameraComponent

class CameraSystem(System):
    def __init__(self, game_state, entity_manager, event_manager, logger):
        super().__init__(game_state, entity_manager, event_manager, logger)
        
        self.logger = logger.loggers['camera_system']

        self.entity_manager.subscribe_to_component(CameraComponent, self.camera_component_callback)

    def camera_component_callback(self, entity, component, action):
        if action == 'add':
            self.entity_manager.entity_with_camera = entity
        elif action == 'remove':
            self.entity_manager.entity_with_camera = None

    def post_event(self, event_type, data):
        self.event_manager.post(Event(event_type, data))

    def get_component(self, entity, component):
        return self.entity_manager.get_component(entity, component)

    def has_component(self, entity, component):
        return self.entity_manager.has_component(entity, component)

    def update(self, delta_time):
        if self.entity_manager.entity_with_camera is not None:
            pass