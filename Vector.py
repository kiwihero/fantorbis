import math
from Position import Position


class Vector:
    """
    The vector functionality
    """

    def __init__(self, orig: Position, dest: Position):
        self.orig = orig
        self.dest = dest

    def magnitude(self):
        """

        :return: Absolute value of vector
        """
        x = self.x_magnitude()
        y = self.y_magnitude()
        mag = math.sqrt(pow(x, 2) + pow(y, 2))
        return abs(mag)

    def set_magnitude(self, magnitude):
        angle = self.angle(degrees=False)
        x_component = math.cos(angle)*magnitude
        y_component = math.sin(angle)*magnitude
        dest = Position(self.orig.x+x_component, self.orig.y+y_component)
        self.dest = dest


    def x_magnitude(self):
        """

        :return: Absolute value of x component
        """
        return abs(self.x_component())

    def y_magnitude(self):
        """
        :return: Absolute value of y component
        """
        return abs(self.y_component())

    def x_component(self):
        """
        X component of vector
        :return:
        """
        orig = self.orig.x
        dest = self.dest.x
        return orig - dest

    def y_component(self):
        """
        Y component of vector
        :return:
        """
        orig = self.orig.y
        dest = self.dest.y
        return orig - dest

    def __str__(self):
        return '{} --> {}'.format(self.orig, self.dest)

    def angle(self, degrees: bool = True):
        """
        Angle of vector
        :param degrees: Boolean - return as degrees or radians
        :return:
        """
        # tangent = opposite/adjacent
        if self.y_component() == 0 or self.x_component() == 0:
            return 0
        tan = self.y_component() / self.x_component()
        angle = math.atan(tan)
        if degrees == True:
            return math.degrees(angle)
        else:
            return angle

    def recenter(self, origin: Position = None):
        """
        Recenter the origin to a given point or 0,0
        :param origin: New origin
        :return:
        """
        x_disp = self.orig.x
        y_disp = self.orig.y
        if origin is not None:
            x_disp -= origin.x
            y_disp -= origin.y
            self.orig.set_position(x=origin.x, y=origin.y)
        else:
            self.orig.set_position(x=0, y=0)
        self.dest.x -= x_disp
        self.dest.y -= y_disp

    def __copy__(self):
        return Vector(self.orig, self.dest)

    def __deepcopy__(self, memodict={}):
        # TODO: Make sure the memo dict is correct to deepcopy a thing
        #  Should I still use __copy__() on the Positions?
        orig = self.orig.__deepcopy__(memodict)
        dest = self.dest.__deepcopy__(memodict)
        return Vector(orig, dest)


import random


# mag = 10
# x1 = random.randint(-1 * mag, mag)
# x2 = random.randint(-1 * mag, mag)
# x3 = random.randint(-1 * mag, mag)
# y1 = random.randint(-1 * mag, mag)
# y2 = random.randint(-1 * mag, mag)
# y3 = random.randint(-1 * mag, mag)
# origin = Position(x1, y1)
# dest = Position(x2, y2)
# v1 = Vector(origin, dest)
# print("V1 {}\nMagnitude {}\nAngle {}".format(v1, v1.magnitude(), v1.angle()))
# v1.recenter()
# print("Recentered V1 {} (angle: {}, magnitude {})".format(v1, v1.angle(), v1.magnitude()))
# o1 = Position(x3, y3)
# v1.recenter(o1)
# print("Recentered V1 {} (angle: {}, magnitude {})".format(v1, v1.angle(), v1.magnitude()))
