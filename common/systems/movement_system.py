# Movement system

from pygame.math import Vector2

from .base_system import System

from common.managers.event_manager import Event

from common.components.acceleration_component import AccelerationComponent
from common.components.collision_component import CollisionComponent
from common.components.collisionevent_component import CollisionEventComponent
from common.components.directionmoving_component import DirectionMovingComponent
from common.components.dashing_component import DashingComponent
from common.components.entitystatus_component import EntityStatusComponent
from common.components.position_component import PositionComponent
from common.components.velocity_component import VelocityComponent

class MovementSystem(System):
    def __init__(self, game_state, entity_manager, event_manager, logger):
        super().__init__(game_state, entity_manager, event_manager, logger)

        self.DECCELERATION_ON_DIRECTION_CHANGE = 8000
        self.DECCELERATION_ON_IDLE = 1000

        self.logger = logger.loggers['movement_system']

    def post_event(self, event_type, data):
        self.event_manager.post(Event(event_type, data))

    def has_component(self, entity, component):
        return self.entity_manager.has_component(entity, component)
    
    def get_component(self, entity, component):
        return self.entity_manager.get_component(entity, component)
    
    def update_acceleration(self, entity, direction_moving_component, acceleration_component):
        acceleration_component.current_acceleration = acceleration_component.max_acceleration * direction_moving_component

    def update_velocity(self, entity, acceleration_component, velocity_component, delta_time):
        current_velocity = velocity_component.current_velocity
        current_acceleration = acceleration_component.current_acceleration
    
        new_velocity = current_velocity + current_acceleration * delta_time
        max_velocity = velocity_component.max_velocity
        if self.has_component(entity, DashingComponent):
            is_dashing = self.get_component(entity, EntityStatusComponent).is_dashing
            if is_dashing:
                max_velocity *= self.get_component(entity, DashingComponent).multiplier
    
        # Apply deceleration for x-axis
        if current_acceleration.x == 0 or (current_acceleration.x < 0 and new_velocity.x > 0) or (current_acceleration.x > 0 and new_velocity.x < 0):
            if new_velocity.x > 0:
                new_velocity.x = max(new_velocity.x - self.DECCELERATION_ON_IDLE * delta_time, 0)
            elif new_velocity.x < 0:
                new_velocity.x = min(new_velocity.x + self.DECCELERATION_ON_IDLE * delta_time, 0)
    
        # Apply deceleration for y-axis
        if current_acceleration.y == 0 or (current_acceleration.y < 0 and new_velocity.y > 0) or (current_acceleration.y > 0 and new_velocity.y < 0):
            if new_velocity.y > 0:
                new_velocity.y = max(new_velocity.y - self.DECCELERATION_ON_IDLE * delta_time, 0)
            elif new_velocity.y < 0:
                new_velocity.y = min(new_velocity.y + self.DECCELERATION_ON_IDLE * delta_time, 0)
    
        # Clamp new_velocity within max and min bounds
        new_velocity.x = max(min(new_velocity.x, max_velocity), -max_velocity)
        new_velocity.y = max(min(new_velocity.y, max_velocity), -max_velocity)
    
        velocity_component.current_velocity = new_velocity

    def update_position(self, entity, delta_time):
        self.entity_manager.get_component(entity, PositionComponent).position += self.entity_manager.get_component(entity, VelocityComponent).current_velocity * delta_time

#?############################################################################## UPDATE FUNCTION ##############################################################################

    def update(self, delta_time):
        # Select components that need to be updated to move
        #TODO Would create a set that adds any components that have moved, and then only update those components
        for entity in (self.entity_manager.component_sets[PositionComponent] &
                    self.entity_manager.component_sets[VelocityComponent] &
                    self.entity_manager.component_sets[AccelerationComponent]):

            # Retrieve necessary components
            velocity_component = self.get_component(entity, VelocityComponent)
            acceleration_component = self.get_component(entity, AccelerationComponent)
            direction_moving_component = self.get_component(entity, DirectionMovingComponent).direction

            # Update acceleration and velocity based on current direction
            self.update_acceleration(entity, direction_moving_component, acceleration_component)
            self.update_velocity(entity, acceleration_component, velocity_component, delta_time)
            
            # check for collisions
            collision_data = self.get_collision_data(entity, delta_time)

            if collision_data["collision_x"] or collision_data["collision_y"]:
                self.handle_collision(entity, collision_data)

            self.update_position(entity, delta_time)

    def get_collision_data(self, entity, delta_time):
        current_position = self.get_component(entity, PositionComponent).position
        current_velocity = self.get_component(entity, VelocityComponent).current_velocity
    
        potential_new_position = current_position + current_velocity * delta_time
    
        # Initially assume no collision
        collision_data = {
            "collision_x": False,
            "collision_y": False,
            "collisions": {},
            "new_position": potential_new_position
        }
    
        # Check for collision in X and Y separately
        potential_position_x = Vector2(potential_new_position.x, current_position.y)
        collision_x = self.check_collision(entity, potential_position_x)
        if collision_x:
            collision_data["collision_x"] = True
            collision_data["collisions"].update(collision_x)
    
        potential_position_y = Vector2(current_position.x, potential_new_position.y)
        collision_y = self.check_collision(entity, potential_position_y)
        if collision_y:
            collision_data["collision_y"] = True
            collision_data["collisions"].update(collision_y)
    
        # If no collision was detected on either axis, check for a corner collision
        if not collision_x and not collision_y:
            collision = self.check_collision(entity, potential_new_position)
            if collision:
                collision_data["collision_x"] = True
                collision_data["collision_y"] = True
                collision_data["collisions"].update(collision)
    
        return collision_data
    
#?#####################################################################################################################################################################

    def handle_collision(self, entity, collision_data):
        self.logger.info(f"Handling collision for {entity} with {collision_data['collisions']}")  # Debugging log
        self.logger.info(collision_data)

        current_position = self.get_component(entity, PositionComponent).position
        current_velocity = self.get_component(entity, VelocityComponent).current_velocity

        final_collision_type = 100
        final_collision_entity = None
        for collision_entity, collision_type in collision_data["collisions"].items():
            if collision_type < final_collision_type:
                final_collision_type = collision_type
                final_collision_entity = collision_entity

        if final_collision_type == 1 or final_collision_type == 100:
            if collision_data["collision_x"] == True:
                current_velocity.x = 0

            if collision_data["collision_y"] == True:
                current_velocity.y = 0

        if self.has_component(final_collision_entity, CollisionEventComponent):
            collision_event_component = self.get_component(final_collision_entity, CollisionEventComponent)
            print(f"Collision event triggered: {collision_event_component.event_name}")

#!#####################################################################################################################################################################

    def check_collision(self, entity, new_position):
        # Create a list to store all the entities that the entity is colliding with
        collisions = {}

        # for now only check components with position and collision, likely will need to have grid system to optimize this as well as on "active status" of the entity
        for other_entity in self.entity_manager.component_sets[PositionComponent] & self.entity_manager.component_sets[CollisionComponent]:
            # Skip the entity itself
            if entity == other_entity:
                continue

            # Check if the entity is colliding with the other entity
            if self.is_colliding(entity, other_entity, new_position):
                collisions[other_entity] = self.get_component(other_entity, CollisionComponent).collision_type
                self.logger.info(f"Collision detected between {entity} and {other_entity}")  # Debugging log

        return collisions

#? MATHS BELOW BEWARD ******************************************************************************

    def dot_product(self, v1, v2):
        """Calculate the dot product of two vectors (tuples)."""
        return v1[0] * v2[0] + v1[1] * v2[1]

    def project_polygon(self, axis, vertices):
        """Project all vertices of the polygon (list of tuples) onto the given axis."""
        min_projection = self.dot_product(vertices[0], axis)
        max_projection = min_projection
        for vertex in vertices[1:]:
            projection = self.dot_product(vertex, axis)
            min_projection = min(min_projection, projection)
            max_projection = max(max_projection, projection)
        return min_projection, max_projection

    def is_overlapping(self, minA, maxA, minB, maxB):
        """Check if two projections on an axis overlap."""
        return minB <= maxA and minA <= maxB

    def translate_polygon(self, polygon, position):
        """Translate a polygon by the given position."""
        return [(point[0] + position.x, point[1] + position.y) for point in polygon]

    def is_colliding(self, entity, other_entity, new_position):
        entity_position = new_position
        other_entity_position = self.get_component(other_entity, PositionComponent).position

        entity_collision_component = self.get_component(entity, CollisionComponent)
        other_collision_component = self.get_component(other_entity, CollisionComponent)

        entity_polygons = entity_collision_component.polygons
        other_polygons = other_collision_component.polygons

        entity_axes = entity_collision_component.axes
        other_axes = other_collision_component.axes

        for poly1, axes1 in zip(entity_polygons, entity_axes):
            translated_poly1 = self.translate_polygon(poly1, entity_position)
            for poly2, axes2 in zip(other_polygons, other_axes):
                translated_poly2 = self.translate_polygon(poly2, other_entity_position)

                for axis in axes1 + axes2:
                    minA, maxA = self.project_polygon(axis, translated_poly1)
                    minB, maxB = self.project_polygon(axis, translated_poly2)
                    # If there's no overlap on this axis, polygons don't collide
                    if not self.is_overlapping(minA, maxA, minB, maxB):
                        break
                else:
                    # If there's overlap on all axes, polygons collide
                    return True
        # If no pair of polygons have overlaps on all axes, polygons don't collide
        return False