import pygame

from .base_system import System

from common.components import ImagesComponent
from common.components import PositionComponent

class RenderSystem(System):
    def __init__(self, game_state, entity_manager, event_manager, logger):
        super().__init__(game_state, entity_manager, event_manager, logger)

        self.logger = logger.loggers['render_system']

        self.screen = game_state.screen

    def update(self, delta_time):
        self.screen.fill((0, 0, 0))

        # Render all entities with images
        for entity in self.entity_manager.entities_to_render.intersection(self.entity_manager.entities_with_image):
            image_component = self.entity_manager.get_component(entity, ImagesComponent)
            images = image_component.images
            current_image = image_component.current_image
            image_to_blit = images[current_image]

            position = self.entity_manager.get_component(entity, PositionComponent).position

            self.screen.blit(image_to_blit, position)

        pygame.display.flip()

        