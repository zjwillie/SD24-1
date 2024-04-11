import pygame
from pygame.math import Vector2

from .base_system import System

from common.components import CameraComponent
from common.components import CollisionComponent
from common.components import FocusPointComponent
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

        
        entities_to_render = self.entity_manager.entities_to_render.intersection(self.entity_manager.entities_with_image)

        # sort by layer, and focus point, need position to calculate offset
        def sorting_key(entity):
            render_layer = self.entity_manager.get_component(entity, RenderComponent).layer
            position = self.entity_manager.get_component(entity, PositionComponent).position
            focus_point = self.entity_manager.get_component(entity, FocusPointComponent).focus_point

            y_compoent = position.y + focus_point.y

            return (render_layer, y_compoent)

        # sort these bad boys
        sorted_entities = sorted(entities_to_render, key=sorting_key)

        for entity in sorted_entities:

            render_component = self.entity_manager.get_component(entity, RenderComponent).render
            if not render_component:
                continue

            # Make sure the entity has images to render, and if not skip it
            if self.entity_manager.get_component(entity, ImageComponent).current_image is None:
                continue

            current_image = self.entity_manager.get_component(entity, ImageComponent).current_image
            image_to_blit = current_image

            position = self.entity_manager.get_component(entity, PositionComponent).position
            image_size = current_image.get_size()

            entity_rect = pygame.Rect(position.x, position.y, image_size[0], image_size[1])
            
            if self.entity_manager.entity_with_camera is None:
                entities_to_blit.append((self.entity_manager.get_component(entity, ImageComponent).current_image, position))

            else:
                # get camera component
                camera_component = self.entity_manager.get_component(self.entity_manager.entity_with_camera, CameraComponent)
                
                # calculate the camera's centered position
                centered_camera_position = Vector2(
                    camera_component.position.x - camera_component.camera_size.x / 2 + self.game_state.resolution[0] / 2, 
                    camera_component.position.y - camera_component.camera_size.y / 2 + self.game_state.resolution[1] / 2
                )
                
                # create the camera's view rectangle
                camera_view = pygame.Rect(centered_camera_position.x, centered_camera_position.y, camera_component.camera_size.x, camera_component.camera_size.y)

                # check if the entity is on the screen
                if camera_view.colliderect(entity_rect):
                    intersection = camera_view.clip(entity_rect)
                    intersetion_image = intersection.move(-position.x, -position.y)
                    image_to_blit = current_image.subsurface(intersetion_image)
                    intersection_screen = intersection.move(-camera_component.position.x, -camera_component.position.y)
                    entities_to_blit.append((image_to_blit, intersection_screen))

        for image, position in entities_to_blit:
            self.screen.blit(image, position)

        for entity in self.entity_manager.entities_with_collision:
            collision_component = self.entity_manager.get_component(entity, CollisionComponent).polygons
            position_component = self.entity_manager.get_component(entity, PositionComponent).position
            for polygon in collision_component:
                offset_polygon = [(point[0] + position_component[0], point[1] + position_component[1]) for point in polygon]
                pygame.draw.polygon(self.screen, (255, 0, 0), offset_polygon, 1)
            
        
        pygame.display.flip()