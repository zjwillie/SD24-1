# ControlComponent.py

from .base_component import Component

class ControlComponent(Component):
    def __init__(self, enabled=False):
        super().__init__()
        # Component initialization
        self.enabled = enabled

