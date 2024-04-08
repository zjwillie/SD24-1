# EntityStatusComponent.py

from .base_component import Component

class EntityStatusComponent(Component):
    def __init__(self):
        super().__init__()
        # Component initialization
        self.is_moving = False
        self.has_moved = False
        self.is_running = False

        self.is_attacking = False
        self.is_dodging = False

        self.is_interacting = False

        self.is_idle = False
        self.is_acting = False

    def reset(self):
        self.is_moving = False
        self.has_moved = False
        self.is_running = False

        self.is_attacking = False
        self.is_dodging = False

        self.is_interacting = False

        self.is_idle = False
        self.is_acting = False
