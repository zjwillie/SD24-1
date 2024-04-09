# FocusPointComponent.py
from pygame.math import Vector2

from .base_component import Component

class FocusPointComponent(Component):
    def __init__(self, x=0, y=0):
        super().__init__()
        # Component initialization
        self.focus_point = Vector2(x, y)
