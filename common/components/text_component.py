# TextComponent.py

from .base_component import Component

class TextComponent(Component):
    def __init__(self, text=None):
        super().__init__()
        # Component initialization
        self.text = text

