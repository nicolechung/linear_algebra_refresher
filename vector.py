from math import sqrt, acos, pi
from decimal import Decimal, getcontext

getcontext().prec = 3

class Vector(object):

    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = 'Cannot normalize the zero vector'
    NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG = 'No unique orthogonal component exists'
    NO_UNIQUE_PARALLEL_COMPONENT_MSG = 'No unique parallel component exists'
    ONLY_DEFINED_IN_THREE_DIMS_MSG = 'Cross product can only be defined in three dimensions'
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')


    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)


    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def plus(self, v):
        new_coordinates = [x+y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def minus(self, v):
        new_coordinates = [x-y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def times_scalar(self, scalar):
        new_coordinates = [Decimal(scalar)*x for x in self.coordinates]
        return Vector(new_coordinates)

    def magnitude(self):
        coordinates_squared = [x**2 for x in self.coordinates]
        return sqrt(sum(coordinates_squared))

    def normalized(self):
        try:
            # Note: need to convert magnitude to a decimal for this
            # to work (video omits this)
            magnitude = Decimal(self.magnitude())
            return self.times_scalar(Decimal('1')/magnitude)

        except ZeroDivisionError:
            raise Exception(self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG)

    def dot(self, v):
        coordinates_multiplied = [x*y for x,y in zip(self.coordinates, v.coordinates)]
        return sum(coordinates_multiplied)

    def angle_with(self, v, in_degrees=False):
        try:
            u1 = self.normalized()
            u2 = v.normalized()

            # acos seems to fail when coordinates are paralle, this is a workaround
            test_parallel = [x == y for x,y in zip(u1.coordinates, u2.coordinates)]
            result = sum(test_parallel)
            if result == len(u1.coordinates):
                return 0

            angle_in_radians = acos(u1.dot(u2))
            if in_degrees:
                degrees_per_radian = 180./ pi
                return angle_in_radians*degrees_per_radian
            else:
                return angle_in_radians

        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception('Cannot compute an angle with the zero vector')
            else:
                raise e

    def is_parallel_to(self, v):
        return self.is_zero() or v.is_zero() or self.angle_with(v) == 0 or self.angle_with(v)  == pi

    def is_orthogonal_to(self, v, tolerance=1e-10):
        return abs(self.dot(v)) < tolerance

    def is_zero(self, tolerance=1e-10):
        return self.magnitude() < tolerance

    def component_parallel_to(self, basis):
        try:
            u = basis.normalized()
            weight = self.dot(u)
            return u.times_scalar(weight)
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG)
            else:
                raise e

    def component_orthogonal_to(self, basis):
        try:
            v_parallel = self.component_parallel_to(basis)
            return self.minus(v_parallel)
        except Exception as e:
            if str(e) == self.NO_UNIQUE_PARALLEL_COMPONENT_MSG:
                raise Exception(self.NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG)
            else:
                raise e

    def cross_product(self, v):
        try:
            x_1, y_1, z_1 = self.coordinates
            x_2, y_2, z_2 = v.coordinates
            new_coordinates = [ y_1*z_2 - y_2*z_1,
                                -(x_1*z_2 - x_2*z_1),
                                x_1*y_2 - x_2*y_1 ]
            return Vector(new_coordinates)

        except ValueError as e:
            msg = str(e)
            if msg == 'not enough values to unpack':
                raise Exception(self.ONLY_DEFINED_IN_THREE_DIMS_MSG)
            else:
                raise e

    def area_of_parallelgram(self, v):
        return (self.cross_product(v)).magnitude()

    def area_of_triangle(self, v):
        return (self.cross_product(v)).magnitude() / Decimal('2.0')

# Example usage for exercises
# v = Vector([5,3,-2])
# w = Vector([-1, 0, 3])
# print('Cross product of v and w', v.cross_product(w))
# print('Area of parallelogram', v.area_of_parallelgram(w))

# v = Vector([8.462, 7.893, -8.187])
# w = Vector([6.984, -5.975, 4.778])
# print('Cross product of v and w', v.cross_product(w))

# v = Vector([-8.987, -9.838, 5.031])
# w = Vector([-4.268, -1.861, -8.866])
# print('Area of parallelogram', v.area_of_parallelgram(w))

# v = Vector([1.5, 9.547, 3.691])
# w = Vector([-6.007, 0.124, 5.772])
# print('Area of triangle', v.area_of_triangle(w))




