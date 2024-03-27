import uuid

from .base_component import Component

class UUIDComponent(Component):
    def __init__(self):
        self.uuid = uuid.uuid4()