"""
This module defines a `Vector` class for representing and performing operations on mathematical vectors.
"""

import array
import random
import operator

class Vector:
    """
    A class representing a mathematical vector with basic operations.
    """

    def __init__(self, *components):
        """
        Initialize the vector with given components.

        :param components: Variable-length argument list of floats representing vector components.
        """
        self._data = array.array('d', components)

    @classmethod
    def random(cls, size=3, min_val=0, max_val = 100):
        """
        Generate a random vector with components in the given range.

        :param size: Number of components in the vector.
        :param min_val: Minimum value of each component.
        :param max_val: Maximum value of each component.
        :return: A new Vector instance with random components.
        """
        return cls(*(random.uniform(min_val, max_val) for _ in range(size)))

    def _check_dimension(self, other):
        if len(self) != len(other):
            raise ValueError("Vectors must have same dimensions")

    def __repr__(self) -> str:
        """
        Return a string representation of the vector.

        :return: A formatted string representing the vector.
        """
        return f"Vector({', '.join(map(str, self._data))})"

    def __len__(self) -> int:
        """
        Return the number of components in the vector.
        
        :return: Integer length of the vector.
        """
        return len(self._data)

    def __getitem__(self, index: int):
        """
        Get the value of a specific component.
        
        :param index: Index of the component.
        :return: Value of the component at the given index.
        """
        return self._data[index]

    def __setitem__(self, index: int, value: float):
        """
        Set the value of a specific component.
        
        :param index: Index of the component.
        :param value: New value for the component.
        """
        _data.index = float(value)

    def __iter__(self):
        """
        Return an iterator over the vector components.
        """
        return iter(self._data)

    def __iadd__(self, other):
        """
        In-place vector addition.
        
        :param other: Another Vector instance.
        :return: Modified Vector instance.
        """
        self._check_dimension(other)
        if isinstance(other, Vector):
            self._data = array.array('d', map(operator.add, self._data, other._data))
 #           for i in range(len(self)):    
#              self._data[i] += other[i]  
        return self
    
    def __isub__(self, other):
        """
        In-place vector subtraction.
        
        :param other: Another Vector instance.
        :return: Modified Vector instance.
        """
        self._check_dimension(other)
        if isinstance(other, Vector):
            self._data = array.array('d', map(operator.sub, self._data, other._data))
        return self

    def __imul__(self, scalar):
        """
        In-place scalar multiplication.
        
        :param scalar: A float value to multiply each component.
        :return: Modified Vector instance.
        """
        if not isinstance(scalar, (float, int)):
            return ValueError("You can only multiply a Vector through scalar.")
        for i in range(len(self)):
            self._data[i] *= scalar
        return self
    
    def __add__(self, other):
        """
        Vector addition.
        
        :param other: Another Vector instance.
        :return: A new Vector instance representing the sum.
        """
        self._check_dimension(other)
        if isinstance(other, Vector):
##          return Vector(*[a + b] for a, b in zip(self,other)) ???????
            return Vector(*(map(operator.add, self._data, other._data)))


    def __sub__(self, other):
        """
        Vector subtraction.
        
        :param other: Another Vector instance.
        :return: A new Vector instance representing the difference.
        """
        self._check_dimension(other)
        if isinstance(other, Vector) and len(self._data):
            return Vector(*(map(operator.sub, self._data, other._data)))
    
    def __mul__(self, scalar):
        """
        Scalar multiplication.
        
        :param scalar: A float value to multiply each component.
        :return: A new Vector instance with scaled components.
        """
        return Vector(*[x * scalar for x in self._data])

        
    def dot(self, other):
        """
        Compute the dot product of two vectors.
        
        :param other: Another Vector instance.
        :return: A float representing the dot product.
        """
        self._check_dimension(other)
        if isinstance(other, Vector):
            return sum(map(operator.mul, self._data, other._data))


    def norm(self):
        """
        Compute the Euclidean norm of the vector.
        
        :return: A float representing the norm.
        """
        return sum(x * x for x in self._data) ** 0.5

    def normalize(self):
        """
        Normalize the vector (scale to unit length).
        
        :return: A new Vector instance representing the normalized vector.
        """
        norm = self.norm()
        return self if norm == 0 else self / norm

    def __eq__(self, other):
        """
        Check if two vectors are equal.
        
        :param other: Another Vector instance.
        :return: True if equal, False otherwise.
        """
        return isinstance(other, Vector) and len(self) == len(other) and all(map(operator.eq, self._data, other._data))

    def __neg__(self):
        """
        Return the negation of the vector.
        
        :return: A new Vector instance with negated components.
        """
        return Vector(*(-x for x in self._data))

    def __abs__(self):
        """
        Return the magnitude of the vector.
        
        :return: A float representing the Euclidean norm.
        """
        return self.norm()


vector1 = Vector(3, 2, 9) 

print(vector1)

