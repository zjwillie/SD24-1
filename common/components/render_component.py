# RenderComponent.py

from .base_component import Component

class RenderComponent(Component):
    def __init__(self, layer, render = True):
        super().__init__()
        self.layer = layer
        self.render = render

