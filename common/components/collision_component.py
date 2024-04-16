# CollisionComponent.py

from .base_component import Component

class CollisionComponent(Component):
    def __init__(self, collision_type=1, polygons=None):
        super().__init__()
        # Component initialization
        self.collision_type = collision_type
        self.polygons = []

        if polygons is not None:
            for polygon in polygons:
                # Convert each dictionary to a tuple and append to self.polygons
                self.polygons.append([(point['x'], point['y']) for point in polygon])
