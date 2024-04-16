# CollisionEventComponent.py

from .base_component import Component

class CollisionEventComponent(Component):
    def __init__(self, event_name=None, event_data=None):
        super().__init__()
        # Component initialization
        self.event_name = event_name
        self.event_data = event_data
        self.had_triggered = False
