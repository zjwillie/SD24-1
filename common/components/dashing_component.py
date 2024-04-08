# DashingComponent.py

from .base_component import Component

class DashingComponent(Component):
    def __init__(self, dashing_multiplier: float = 1.0):
        super().__init__()
        # Component initialization
        self.dashing_multiplier = dashing_multiplier
