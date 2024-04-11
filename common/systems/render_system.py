import pygame
from pygame.math import Vector2

from .base_system import System
from common.components import (
    CameraComponent,
    CollisionComponent,
    FocusPointComponent,
    ImageComponent,
    PositionComponent,
    RenderComponent,
)

class RenderSystem(System):
    def __init__(self, game_state, entity_manager, event_manager, logger):
        super().__init__(game_state, entity_manager, event_manager, logger)
        self.logger = logger.loggers['render_system']
        self.screen = game_state.screen

    def update(self, delta_time):
        self.clear_screen()

        entities_to_blit = self.get_entities_to_render()
        self.blit_entities(entities_to_blit)
        self.draw_collisions()

        pygame.display.flip()

    def clear_screen(self):
        self.screen.fill((0, 0, 0))

    def get_entities_to_render(self):
        entities_to_blit = []
        entities_to_render = self.entity_manager.entities_to_render.intersection(self.entity_manager.entities_with_image)
        sorted_entities = self.sort_entities_by_layer_and_focus_point(entities_to_render)
        for entity in sorted_entities:
            blit_info = self.get_entity_blit_info(entity)
            if blit_info:
                entities_to_blit.append(blit_info)
        return entities_to_blit

    def sort_entities_by_layer_and_focus_point(self, entities):
        def sorting_key(entity):
            render_layer = self.entity_manager.get_component(entity, RenderComponent).layer
            position = self.entity_manager.get_component(entity, PositionComponent).position
            focus_point = self.entity_manager.get_component(entity, FocusPointComponent).focus_point
            return (render_layer, position.y + focus_point.y)
        return sorted(entities, key=sorting_key)

    def get_entity_blit_info(self, entity):
        render_component = self.entity_manager.get_component(entity, RenderComponent).render
        if not render_component or self.entity_manager.get_component(entity, ImageComponent).current_image is None:
            return None

        current_image = self.entity_manager.get_component(entity, ImageComponent).current_image
        position = self.entity_manager.get_component(entity, PositionComponent).position
        if self.entity_manager.entity_with_camera is None:
            return (current_image, position)
        else:
            return self.get_camera_adjusted_blit_info(entity, current_image, position)

    def get_camera_adjusted_blit_info(self, entity, current_image, position):
        camera_component = self.entity_manager.get_component(self.entity_manager.entity_with_camera, CameraComponent)
        entity_rect = pygame.Rect(position.x, position.y, *current_image.get_size())
        camera_view = self.get_camera_view_rect(camera_component)

        if camera_view.colliderect(entity_rect):
            intersection = camera_view.clip(entity_rect)
            intersection_image = intersection.move(-position.x, -position.y)
            image_to_blit = current_image.subsurface(intersection_image)

            # Adjust the intersection position with the camera offset
            screen_position = Vector2(intersection.topleft) - Vector2(camera_component.position) + Vector2(camera_component.offset)
            return (image_to_blit, screen_position)
        return None

    def get_camera_view_rect(self, camera_component):
        # This creates a rectangle representing the camera's view in the game world
        return pygame.Rect(
            camera_component.position.x, 
            camera_component.position.y, 
            camera_component.camera_size.x, 
            camera_component.camera_size.y
        )

    def blit_entities(self, entities_to_blit):
        for image, position in entities_to_blit:
            self.screen.blit(image, position)

    def draw_collisions(self):
        camera_component = self.entity_manager.get_component(self.entity_manager.entity_with_camera, CameraComponent)
        for entity in self.entity_manager.entities_with_collision:
            collision_component = self.entity_manager.get_component(entity, CollisionComponent).polygons
            position_component = self.entity_manager.get_component(entity, PositionComponent).position
            for polygon in collision_component:
                # Adjust polygon points with the camera offset and convert them to tuples
                offset_polygon = [
                    (Vector2(point) + position_component - camera_component.position + camera_component.offset).xy for point in polygon
                ]
                pygame.draw.polygon(self.screen, (255, 0, 0), offset_polygon, 1)
