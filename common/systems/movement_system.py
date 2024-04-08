# Movement system

from .base_system import System

from common.managers.event_manager import Event

from common.components.acceleration_component import AccelerationComponent
from common.components.directionmoving_component import DirectionMovingComponent
from common.components.position_component import PositionComponent
from common.components.velocity_component import VelocityComponent

class MovementSystem(System):
    def __init__(self, game_state, entity_manager, event_manager, logger):
        super().__init__(game_state, entity_manager, event_manager, logger)

        self.logger = logger.loggers['movement_system']

    def post_event(self, event_type, data):
        self.event_manager.post(Event(event_type, data))

    def has_component(self, entity, component):
        return self.entity_manager.has_component(entity, component)
    
    def get_component(self, entity, component):
        return self.entity_manager.get_component(entity, component)
    
    def apply_direction_to_acceleration(self, entity, direction_moving_component, acceleration_component):
        self.get_component(entity, AccelerationComponent).current_acceleration = acceleration_component.max_acceleration * direction_moving_component

    def apply_acceleration_to_velocity(self, entity, acceleration_component, velocity_component, delta_time):
        new_velocity = velocity_component.current_velocity + acceleration_component.current_acceleration * delta_time
        if new_velocity.magnitude() > velocity_component.max_velocity:
            new_velocity = new_velocity.normalize() * velocity_component.max_velocity
        self.get_component(entity, VelocityComponent).current_velocity = new_velocity


    def update(self, delta_time):
        for entity in self.entity_manager.entities_with_position & self.entity_manager.entities_with_velocity & self.entity_manager.entities_with_acceleration:
            acceleration_component = self.get_component(entity, AccelerationComponent)
            velocity_component = self.get_component(entity, VelocityComponent)
            position_component = self.get_component(entity, PositionComponent)
            direction_moving_component = self.get_component(entity, DirectionMovingComponent).direction
            
            self.apply_direction_to_acceleration(entity, direction_moving_component, acceleration_component)

            self.apply_acceleration_to_velocity(entity, acceleration_component, velocity_component, delta_time)
            self.logger.info(f"Direction: {direction_moving_component}, Acceleration: {acceleration_component.current_acceleration}, Velocity: {velocity_component.current_velocity}, Position: {position_component.position}")
            
