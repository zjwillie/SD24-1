# CollisionComponent.py

from .base_component import Component

class CollisionComponent(Component):
    # Collision types
    STOP_SLIDE = 1
    STOP_FULL = 2
    BOUNCE = 3
    TRIGGER_EVENT = 10

    def __init__(self, polygons=None, collision_type=STOP_SLIDE):
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
    
    def subtract_vectors(self, vector1, vector2):
        """Subtract vector v2 from v1, where vectors are tuples."""
        return (vector1[0] - vector2[0], vector1[1] - vector2[1])
    
    def perpendicular_vector(self, vector):
        """Get a vector (tuple) that is perpendicular to the given vector v."""
        return (-vector[1], vector[0])
    
    def normalize_vector(self, vector):
        """Normalize the given vector v, which is a tuple."""
        length = (vector[0] ** 2 + vector[1] ** 2) ** 0.5
        if length == 0:
            return (0, 0)  # To avoid division by zero
        return (vector[0] / length, vector[1] / length)