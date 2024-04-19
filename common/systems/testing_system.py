import math
import random

from pygame.math import Vector2

from .base_system import System

from common.managers.event_manager import Event

from common.components.acceleration_component import AccelerationComponent
from common.components.collision_component import CollisionComponent
from common.components.directionmoving_component import DirectionMovingComponent
from common.components.position_component import PositionComponent
from common.components.testingcollision_component import TestingCollisionComponent
from common.components.velocity_component import VelocityComponent

""" In case we want it later
            "_testing/_testing_bit.json",
            "_testing/_testing_bit_32x32.json",
            "_testing/_testing_bit_64x64.json",
            "_testing/_testing_bit_32x32_1.json",
            "_testing/_testing_bit_32x32_2.json",
            "_testing/_testing_bit_32x32_3.json",
            "_testing/_testing_bit_32x32_4.json",
            "_testing/_testing_bit_32x32_5.json",
            "_testing/_testing_bit_32x32_6.json",
            "_testing/_testing_bit_32x32_7.json",
            "_testing/_testing_bit_32x32_8.json",
            "_testing/_testing_bit_32x32_9.json",
            "_testing/_testing_bit_32x32_10.json",
            "_testing/_testing_bit_32x32_11.json"
"""

class TestingSystem(System):
    def __init__(self, game_state, entity_manager, event_manager, logger):
        super().__init__(game_state, entity_manager, event_manager, logger)
        
        self.logger = logger.loggers['testing_system']

        def random_polygon(max_size, num_points):
            points = []
            for _ in range(num_points):
                x = random.randint(0, max_size)
                y = random.randint(0, max_size)
                points.append((x, y))

            # Calculate the centroid of the points
            centroid = (sum(x for x, y in points) / num_points, sum(y for x, y in points) / num_points)

            # Sort the points by their angle relative to the centroid
            points.sort(key=lambda point: math.atan2(point[1] - centroid[1], point[0] - centroid[0]))

            return [{'x': x, 'y': y} for x, y in points]

        num_entities = 20
        num_columns = math.ceil(math.sqrt(num_entities))
        num_rows = math.ceil(num_entities / num_columns)
        cell_width = 800 / num_columns
        cell_height = 600 / num_rows

        for i in range(num_entities):
            entity = self.entity_manager.create_entity()
            self.entity_manager.add_component(entity, DirectionMovingComponent())
            self.entity_manager.add_component(entity, TestingCollisionComponent())

            # Spread the entities evenly across the 800x600 area
            position = Vector2((i % num_columns) * cell_width + cell_width / 2, (i // num_columns) * cell_height + cell_height / 2)
            self.entity_manager.add_component(entity, PositionComponent(position))

            self.entity_manager.add_component(entity, VelocityComponent(random.randint(100, 550)))
            self.entity_manager.add_component(entity, AccelerationComponent(2000))

            num_points = random.randint(3, 7)
            polygon = random_polygon(64, num_points)

            self.entity_manager.add_component(entity, CollisionComponent(CollisionComponent.STOP_SLIDE, polygons=[polygon]))




    def post_event(self, event_type, data):
        self.event_manager.post(Event(event_type, data))

    def get_component(self, entity, component):
        return self.entity_manager.get_component(entity, component)

    def has_component(self, entity, component):
        return self.entity_manager.has_component(entity, component)

    def update(self, delta_time):
        for entity in self.entity_manager.component_sets[TestingCollisionComponent]:
            self.get_component(entity, DirectionMovingComponent).direction = Vector2(random.randint(-1, 1), random.randint(-1, 1))
