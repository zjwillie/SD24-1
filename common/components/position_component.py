# PositionComponent.py

from .base_component import Component
from pygame.math import Vector2

class PositionComponent(Component):
    def __init__(self, x=0, y=0):
        super().__init__()
        self.position = Vector2(x, y)
