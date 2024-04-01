# IDComponent.py

from .base_component import Component

class IDComponent(Component):
    def __init__(self, id=None):
        super().__init__()
        self.id = id

