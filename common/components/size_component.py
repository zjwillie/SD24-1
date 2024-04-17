# SizeComponent.py

from .base_component import Component

class SizeComponent(Component):
    def __init__(self, width, height):
        super().__init__()
        # Component initialization
        self.width = width
        self.height = height

