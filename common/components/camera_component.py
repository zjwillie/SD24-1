from pygame.math import Vector2
from pygame.rect import Rect

from .base_component import Component

class CameraComponent(Component):
    def __init__(self, position=(0, 0), camera_size=(0, 0), world_size=(0, 0), dead_zone=(20, 20, 20, 20), offset=(0, 0)):
        super().__init__()

        # If the arguments are tuples, convert them to Vector2 or Rect objects
        if isinstance(position, tuple):
            position = Vector2(*position)
        if isinstance(camera_size, tuple):
            camera_size = Vector2(*camera_size)
        if isinstance(world_size, tuple):
            world_size = Vector2(*world_size)
        if isinstance(dead_zone, tuple):
            dead_zone = Rect(*dead_zone)
        if isinstance(offset, tuple):
            offset = Vector2(*offset)

        self.position = position
        self.camera_size = camera_size
        self.world_size = world_size
        self.dead_zone = dead_zone
        self.offset = offset  # Use the passed offset or default to (0, 0)

        #print("CameraComponent initialized")
