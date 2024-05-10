# TextBoxComponent.py
from pygame import Vector2

from .base_component import Component

class TextBoxComponent(Component):
    def __init__(self, font, border, width, height, x, y):
        super().__init__()
        
        self.font = font
        self.border = border
        self.width = width
        self.height = height
        self.location = Vector2(x, y)

