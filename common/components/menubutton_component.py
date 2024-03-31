# MenuButtonComponent.py

from .base_component import Component

class MenuButtonComponent(Component):
    def __init__(self, menu_action):
        self.menu_action = menu_action