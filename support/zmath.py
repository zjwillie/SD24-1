class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        elif isinstance(other, tuple) and len(other) == 2:
            return Vector(self.x + other[0], self.y + other[1])
        else:
            raise TypeError("Unsupported type for addition with Vector")
    
    def __sub__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)
        elif isinstance(other, tuple) and len(other) == 2:
            return Vector(self.x - other[0], self.y - other[1])
        else:
            raise TypeError("Unsupported type for subtraction with Vector")

    def __mul__(self, scalar):
        if isinstance(scalar, (int, float)):
            return Vector(self.x * scalar, self.y * scalar)
        else:
            raise TypeError("Unsupported type for multiplication with Vector")

    def __truediv__(self, scalar):
        if isinstance(scalar, (int, float)):
            return Vector(self.x / scalar, self.y / scalar)
        else:
            raise TypeError("Unsupported type for division with Vector")
 
    def __floordiv__(self, scalar):
        if isinstance(scalar, (int, float)):
            return Vector(self.x // scalar, self.y // scalar)
        else:
            raise TypeError("Unsupported type for floor division with Vector")
    
    def __eq__(self, other):
        if isinstance(other, Vector):
            return self.x == other.x and self.y == other.y
        elif isinstance(other, tuple) and len(other) == 2:
            return self.x == other[0] and self.y == other[1]
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def __repr__(self):
        return f"vector({self.x}, {self.y})"
    
    def magnitude(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5
    
    def normalize(self):
        magnitude = self.magnitude()
        if magnitude > 0:
            return Vector(self.x / magnitude, self.y / magnitude)
        return Vector(0, 0)

    def dot(self, other):
        if isinstance(other, Vector):
            return self.x * other.x + self.y * other.y
        elif isinstance(other, tuple) and len(other) == 2:
            return self.x * other[0] + self.y * other[1]
        else:
            raise TypeError("Unsupported type for dot product with Vector")

    def distance_to(self, other):
        if isinstance(other, Vector):
            return (self - other).magnitude()
        elif isinstance(other, tuple) and len(other) == 2:
            return (self - Vector(*other)).magnitude()
        else:
            raise TypeError("Unsupported type for distance calculation with Vector")