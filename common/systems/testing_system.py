import random

from pygame.math import Vector2

from .base_system import System

from common.managers.event_manager import Event

from common.components.directionmoving_component import DirectionMovingComponent
from common.components.testingcollision_component import TestingCollisionComponent

class TestingSystem(System):
    def __init__(self, game_state, entity_manager, event_manager, logger):
        super().__init__(game_state, entity_manager, event_manager, logger)
        
        self.logger = logger.loggers['testing_system']

    def post_event(self, event_type, data):
        self.event_manager.post(Event(event_type, data))

    def get_component(self, entity, component):
        return self.entity_manager.get_component(entity, component)

    def has_component(self, entity, component):
        return self.entity_manager.has_component(entity, component)

    def update(self, delta_time):
        for entity in self.entity_manager.component_sets[TestingCollisionComponent]:
            self.get_component(entity, DirectionMovingComponent).direction = Vector2(random.randint(-1, 1), random.randint(-1, 1))
