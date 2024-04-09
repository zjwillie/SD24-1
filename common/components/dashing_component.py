# DashingComponent.py

from .base_component import Component

class DashingComponent(Component):
    def __init__(self, multiplier: float = 1.0):
        super().__init__()
        # Component initialization
        self.multiplier = multiplier
