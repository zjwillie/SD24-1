# CollisionComponent.py

from .base_component import Component

class CollisionComponent(Component):
    def __init__(self, polygons=None):
        super().__init__()
        # Component initialization
        self.polygons = []

        if polygons is not None:
            for polygon in polygons:
                # Convert each dictionary to a tuple and append to self.polygons
                self.polygons.append([(point['x'], point['y']) for point in polygon])

        print(f"Collision Component Initialized: {self.polygons}")
