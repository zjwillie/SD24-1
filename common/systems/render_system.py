import pygame

from .base_system import System

from common.components import ImagesComponent
from common.components import PositionComponent
from common.components import RenderComponent

class RenderSystem(System):
    def __init__(self, game_state, entity_manager, event_manager, logger):
        super().__init__(game_state, entity_manager, event_manager, logger)

        self.logger = logger.loggers['render_system']

        self.screen = game_state.screen

    def update(self, delta_time):
        self.screen.fill((0, 0, 0))

        # Render all entities with images
        entities_to_blit = []
        for entity in sorted(self.entity_manager.entities_to_render.intersection(self.entity_manager.entities_with_image), 
                             key=lambda entity: self.entity_manager.get_component(entity, RenderComponent).layer):

            render_component = self.entity_manager.get_component(entity, RenderComponent).render
            if not render_component:
                continue
            
            image_component = self.entity_manager.get_component(entity, ImagesComponent)
            images = image_component.images
            current_image = image_component.current_image
            image_to_blit = images[current_image]

            position = self.entity_manager.get_component(entity, PositionComponent).position

            entities_to_blit.append((image_to_blit, position))

        for image, position in entities_to_blit:
            self.screen.blit(image, position)

        pygame.display.flip()
        