# TextBoxComponent.py
from pygame import Vector2

from .base_component import Component

class TextBoxComponent(Component):
    def __init__(self, font, border, arrows, width, height, x, y):
        super().__init__()
        
        self.font = None
        self.border = None
        self.arrows = None
        self.width = 0
        self.height = 0
        self.location = Vector2(0, 0)

