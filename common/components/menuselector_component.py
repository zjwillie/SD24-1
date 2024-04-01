# MenuSelectorComponent.py

from .base_component import Component

class MenuSelectorComponent(Component):
    def __init__(self, options):
        self.options = options
        self.current_selection = 0
