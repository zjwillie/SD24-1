# CollisionComponent.py

from .base_component import Component

class CollisionComponent(Component):
    # Collision types
    STOP_SLIDE = 1
    STOP_FULL = 2
    BOUNCE = 3
    TRIGGER_EVENT = 10

    def __init__(self, collision_type=STOP_SLIDE, polygons=None):
        super().__init__()
        # Component initialization
        self.collision_type = collision_type
        self.polygons = []

        if polygons is not None:
            for polygon in polygons:
                # Convert each dictionary to a tuple and append to self.polygons
                self.polygons.append([(point['x'], point['y']) for point in polygon])

        self.axes = [self.get_axes(poly) for poly in self.polygons]

    def get_axes(self, vertices):
        axes = []
        for i in range(len(vertices)):
            p1 = vertices[i]
            p2 = vertices[(i + 1) % len(vertices)]  # Wrap around to the first vertex
            edge = self.subtract_vectors(p2, p1)
            normal = self.perpendicular_vector(edge)
            axes.append(self.normalize_vector(normal))
        return axes
    
    def subtract_vectors(self, v1, v2):
        """Subtract vector v2 from v1, where vectors are tuples."""
        return (v1[0] - v2[0], v1[1] - v2[1])
    
    def perpendicular_vector(self, v):
        """Get a vector (tuple) that is perpendicular to the given vector v."""
        return (-v[1], v[0])
    
    def normalize_vector(self, v):
        """Normalize the given vector v, which is a tuple."""
        length = (v[0] ** 2 + v[1] ** 2) ** 0.5
        if length == 0:
            return (0, 0)  # To avoid division by zero
        return (v[0] / length, v[1] / length)