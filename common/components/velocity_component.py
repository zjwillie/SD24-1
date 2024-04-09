# VelocityComponent.py
from pygame.math import Vector2

from .base_component import Component

class VelocityComponent(Component):
    def __init__(self, max_velocity=0):
        super().__init__()
        # Component initialization
        self.current_velocity = Vector2(0, 0)
        self.max_velocity = max_velocity

