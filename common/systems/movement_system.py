# Movement system

from .base_system import System

from common.managers.event_manager import Event

from common.components.acceleration_component import AccelerationComponent
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
            self.logger.info(f"Direction: {direction_moving_component}, Acceleration: {acceleration_component.current_acceleration}, Velocity: {velocity_component.current_velocity}, Position: {position_component.position}")
            
            self.update_position(entity, velocity_component, position_component, delta_time)
