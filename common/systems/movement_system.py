# Movement system

from pygame.math import Vector2

from .base_system import System

from common.managers.event_manager import Event

from common.components.acceleration_component import AccelerationComponent
from common.components.collision_component import CollisionComponent
from common.components.directionmoving_component import DirectionMovingComponent
from common.components.dashing_component import DashingComponent
from common.components.entitystatus_component import EntityStatusComponent
from common.components.position_component import PositionComponent
from common.components.velocity_component import VelocityComponent

class MovementSystem(System):
    def __init__(self, game_state, entity_manager, event_manager, logger):
        super().__init__(game_state, entity_manager, event_manager, logger)

        self.DECCELERATION_ON_DIRECTION_CHANGE = 4000
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
        if current_acceleration.x == 0:
            if new_velocity.x > 0:
                new_velocity.x = max(new_velocity.x - self.DECCELERATION_ON_IDLE * delta_time, 0)
            elif new_velocity.x < 0:
                new_velocity.x = min(new_velocity.x + self.DECCELERATION_ON_IDLE * delta_time, 0)

        # Apply deceleration for y-axis
        if current_acceleration.y == 0:
            if new_velocity.y > 0:
                new_velocity.y = max(new_velocity.y - self.DECCELERATION_ON_IDLE * delta_time, 0)
            elif new_velocity.y < 0:
                new_velocity.y = min(new_velocity.y + self.DECCELERATION_ON_IDLE * delta_time, 0)
        
        # Deceleration when changing direction
        if (new_velocity.x > 0 and current_velocity.x < 0) or (new_velocity.x < 0 and current_velocity.x > 0):
            if current_velocity.x > 0:
                new_velocity.x -=  self.DECCELERATION_ON_DIRECTION_CHANGE * delta_time
            elif current_velocity.x < 0:
                new_velocity.x +=  self.DECCELERATION_ON_DIRECTION_CHANGE * delta_time
        if (new_velocity.y > 0 and current_velocity.y < 0) or (new_velocity.y < 0 and current_velocity.y > 0):
            if current_velocity.y > 0:
                new_velocity.y -=  self.DECCELERATION_ON_DIRECTION_CHANGE * delta_time
            elif current_velocity.y < 0:
                new_velocity.y +=  self.DECCELERATION_ON_DIRECTION_CHANGE * delta_time

        # Clamp new_velocity within max and min bounds
        new_velocity.x = max(min(new_velocity.x, max_velocity), -max_velocity)
        new_velocity.y = max(min(new_velocity.y, max_velocity), -max_velocity)

        velocity_component.current_velocity = new_velocity

    def update_position(self, entity, velocity_component, position_component, delta_time):
        position_component.position.x += velocity_component.current_velocity.x * delta_time
        position_component.position.y += velocity_component.current_velocity.y * delta_time

    def update(self, delta_time):
        for entity in self.entity_manager.entities_with_position & self.entity_manager.entities_with_velocity & self.entity_manager.entities_with_acceleration:
            acceleration_component = self.get_component(entity, AccelerationComponent)
            velocity_component = self.get_component(entity, VelocityComponent)
            position_component = self.get_component(entity, PositionComponent)
            direction_moving_component = self.get_component(entity, DirectionMovingComponent).direction
            
            self.update_acceleration(entity, direction_moving_component, acceleration_component)

            self.update_velocity(entity, acceleration_component, velocity_component, delta_time)
            #self.logger.info(f"Direction: {direction_moving_component}, Acceleration: {acceleration_component.current_acceleration}, Velocity: {velocity_component.current_velocity}, Position: {position_component.position}")
            
            self.check_collision(entity, position_component)

            self.update_position(entity, velocity_component, position_component, delta_time)

    def check_collision(self, entity, position_component):
        collisions = []
        for other_entity in self.entity_manager.entities_with_position & self.entity_manager.entities_with_collision:
            if entity == other_entity:
                continue
            if self.is_colliding(entity, other_entity):
                collisions.append(other_entity)
                self.logger.info(f"Collision detected between {entity} and {other_entity}")  # Debugging log

        if len(collisions) > 0:
            self.post_event("collision", {"entity": entity, "collisions": collisions})
            for other_entity in collisions:
                self.handle_collision(entity, other_entity)

    def handle_collision(self, entity, other_entity):
        # Set velocity of entity to 0
        velocity_component = self.get_component(entity, VelocityComponent)
        velocity_component.current_velocity = Vector2(0, 0)

        # Get the positions of the two entities
        position_component = self.get_component(entity, PositionComponent)
        other_position_component = self.get_component(other_entity, PositionComponent)

        # Calculate the direction from the other entity to the current entity
        direction = position_component.position - other_position_component.position

        # Normalize the direction
        direction.normalize_ip()

        # Move the current entity out of collision
        position_component.position += direction


    def subtract_vectors(self, v1, v2):
        """Subtract vector v2 from v1, where vectors are tuples."""
        return (v1[0] - v2[0], v1[1] - v2[1])

    def perpendicular_vector(self, v):
        """Get a vector (tuple) that is perpendicular to the given vector v."""
        return (-v[1], v[0])

    def normalize_vector(self, v):
        """Normalize the given vector v, which is a tuple."""
        length = (v[0] ** 2 + v[1] ** 2) ** 0.5
        if length == 0:
            return (0, 0)  # To avoid division by zero
        return (v[0] / length, v[1] / length)

    def dot_product(self, v1, v2):
        """Calculate the dot product of two vectors (tuples)."""
        return v1[0] * v2[0] + v1[1] * v2[1]

    def get_axes(self, vertices):
        """Get all the axes to test for SAT by finding normals to the polygon's edges."""
        axes = []
        for i in range(len(vertices)):
            p1 = vertices[i]
            p2 = vertices[(i + 1) % len(vertices)]  # Wrap around to the first vertex
            edge = self.subtract_vectors(p2, p1)
            normal = self.perpendicular_vector(edge)
            axes.append(self.normalize_vector(normal))
        return axes

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

    def is_colliding(self, entity, other_entity):
        entity_position = self.get_component(entity, PositionComponent).position
        other_entity_position = self.get_component(other_entity, PositionComponent).position

        entity_polygons = self.get_component(entity, CollisionComponent).polygons
        other_polygons = self.get_component(other_entity, CollisionComponent).polygons

        for poly1 in entity_polygons:
            translated_poly1 = self.translate_polygon(poly1, entity_position)
            for poly2 in other_polygons:
                translated_poly2 = self.translate_polygon(poly2, other_entity_position)

                axes1 = self.get_axes(translated_poly1)
                axes2 = self.get_axes(translated_poly2)
                for axis in axes1 + axes2:
                    minA, maxA = self.project_polygon(axis, translated_poly1)
                    minB, maxB = self.project_polygon(axis, translated_poly2)
                    if not self.is_overlapping(minA, maxA, minB, maxB):
                        # If there's no overlap on this axis, polygons don't collide
                        return False
        # If all axes have overlaps, polygons collide
        return True