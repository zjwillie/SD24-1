# DirectionFacingComponent.py

from .base_component import Component

class DirectionFacingComponent(Component):
    def __init__(self, direction=None):
        super().__init__()
        # Component initialization
        self.direction = direction
