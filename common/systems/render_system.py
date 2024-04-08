import pygame

from .base_system import System

from common.components import CollisionComponent
from common.components import ImageComponent
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

            # Make sure the entity has images to render, and if not skip it
            if self.entity_manager.get_component(entity, ImageComponent).current_image is None:
                continue
            
            current_image = self.entity_manager.get_component(entity, ImageComponent).current_image
            image_to_blit = current_image

            position = self.entity_manager.get_component(entity, PositionComponent).position

            #TODO Need to not draw that which is not on the screen
            entities_to_blit.append((image_to_blit, position))

        for image, position in entities_to_blit:
            self.screen.blit(image, position)

        for entity in self.entity_manager.entities_with_collision:
            collision_component = self.entity_manager.get_component(entity, CollisionComponent).polygons
            position_component = self.entity_manager.get_component(entity, PositionComponent).position
            for polygon in collision_component:
                offset_polygon = [(point[0] + position_component[0], point[1] + position_component[1]) for point in polygon]
                pygame.draw.polygon(self.screen, (255, 0, 0), offset_polygon, 1)
            
        
        pygame.display.flip()