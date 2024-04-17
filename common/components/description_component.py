# DescriptionComponent.py

from .base_component import Component

class DescriptionComponent(Component):
    def __init__(self, description=None):
        super().__init__()
        # Component initialization
        self.description = description
