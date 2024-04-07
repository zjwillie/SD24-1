# DirectionMovingComponent.py

from pygame.math import Vector2

from .base_component import Component


class DirectionMovingComponent(Component):
    def __init__(self, direction = (0,0)):
        super().__init__()
        self.direction = Vector2(direction)

