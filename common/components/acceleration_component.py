# AccelerationComponent.py
from pygame.math import Vector2

from .base_component import Component

class AccelerationComponent(Component):
    def __init__(self, max_acceleration=0):
        super().__init__()
        # Component initialization
        self.current_acceleration = Vector2(0, 0)
        self.max_acceleration = max_acceleration

