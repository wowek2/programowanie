import math
import random

class Vector:
    
    def __init__(self, *components):
        self.components = list(components)
        
    @classmethod
    def random(cls, size=3, min_val=0, max_val=100):
        return cls(*[random.uniform(min_val, max_val) for _ in range(size)])
    
    def __repr__(self):
        return f"Vector({', '.join(map(str, self.components))})"
    
    def __len__(self):
        return len(self.components)
    
    def __getitem__(self, index):
        return self.components[index]
    
    def __setitem__(self, index, value):
        self.components[index] = float(value)
    
    def __iter__(self):
        return iter(self.components)
    
    def _check_dimension(self, other):
        if len(self) != len(other):
            raise ValueError("Vectors must have same dimensions")
    
    def __add__(self, other):
        self._check_dimension(other)
        return Vector(*[a + b for a, b in zip(self, other)])
    
    def __sub__(self, other):
        self._check_dimension(other)
        return Vector(*[a - b for a, b in zip(self, other)])
    
    def __mul__(self, scalar):
        return Vector(*[x * scalar for x in self.components])
    
    def dot(self, other):
        if not isinstance(other, Vector):
            raise TypeError("Dot product requires another Vector")
        self._check_dimension(other)
        return sum(a * b for a, b in zip(self, other))
    
    def norm(self):
        return math.sqrt(sum(x**2 for x in self.components))
    
    def normalize(self):
        length = self.norm()
        if length == 0:
            return Vector(*[0.0]*len(self))
        return self / length
    
    def __eq__(self, other):
        return (isinstance(other, Vector) and 
                len(self) == len(other) and 
                all(a == b for a, b in zip(self, other)))
    
    def __neg__(self):
        return Vector(*[-x for x in self.components])
    
    def __abs__(self):
        return self.norm()
    
    def __iadd__(self, other):
        self._check_dimension(other)
        for i in range(len(self)):
            self.components[i] += other[i]
        return self
    
    def __isub__(self, other):
        self._check_dimension(other)
        for i in range(len(self)):
            self.components[i] -= other[i]
        return self
    
    def __imul__(self, scalar):
        for i in range(len(self)):
            self.components[i] *= scalar
        return self