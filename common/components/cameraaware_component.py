# CameraAwareComponent.py

from .base_component import Component

class CameraAwareComponent(Component):
    def __init__(self, is_dynamic=False):
        super().__init__()
        self.is_dynamic = is_dynamic

