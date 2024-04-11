# Camera System
from pygame.math import Vector2

from .base_system import System

from common.managers.event_manager import Event

from common.components.camera_component import CameraComponent
from common.components.position_component import PositionComponent

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

    def smoothsetp(self, x):
        return x * x * (3 - 2 * x)

    def update(self, delta_time):
        if self.entity_manager.entity_with_camera is not None:
            camera_component = self.get_component(self.entity_manager.entity_with_camera, CameraComponent)
            target_position = self.get_component(self.entity_manager.entity_with_camera, PositionComponent).position

            camera_center = camera_component.position + camera_component.camera_size / 2

            deadzone = camera_component.dead_zone
            deadzone.center = camera_center

            if not deadzone.collidepoint(target_position.x, target_position.y):
                target_relative_position = target_position - Vector2(deadzone.center)

                distance = target_relative_position.length()
                if distance > 0:
                    if distance > 10:
                        factor = self.smoothsetp(min(distance / 100, 1))

                        camera_component.position += target_relative_position * factor * 0.1

                # previously converted back to pygame.vect but shoud not need here

        camera_component.position.x = max(0, int(min(camera_component.world_size.x - camera_component.camera_size.x, camera_component.position.x)))
        camera_component.position.y = max(0, int(min(camera_component.world_size.y - camera_component.camera_size.y, camera_component.position.y)))

        self.logger.info(f"Camera Position: {camera_component.position}")
