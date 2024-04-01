# RenderComponent.py

from .base_component import Component

class RenderComponent(Component):
    def __init__(self, layer, should_render = True):
        super().__init__()
        self.layer = layer

