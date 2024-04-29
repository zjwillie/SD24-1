# TextBoxComponent.py
from pygame import Vector2

from .base_component import Component

class TextBoxComponent(Component):
    def __init__(self):
        super().__init__()
        self.dialogue = None
        self.responses = []
        
        self.font = None
        self.border = None
        self.arrows = None
        self.width = 0
        self.height = 0
        self.location = Vector2(0, 0)
