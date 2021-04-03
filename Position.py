from typing import Union, Type

class Position:
    """
    The position functionality
    """

    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def change_position(self, position_object: 'Position' = None, x: int = 0, y: int = 0):
        """
        Relative movement
        Can give either x and y, or another position object
        :param position_object:
        :param x: self.x is changed by this much
        :param y: self.y is changed by this much
        :return: this Position object
        """
        if position_object is not None:
            self.x += position_object.x
            self.y += position_object.y
        else:
            self.x += x
            self.y += y
        return self

    def set_position(self, position_object: 'Position' = None, x: int = None, y: int = None):
        """
        Absolute movement
        Can give either x and y, or another position object
        :param position_object:
        :param x: self.x is now this value, regardless of previous position
        :param y: self.y is now this value, regardless of previous position
        :return: this Position object
        """
        if position_object is not None:
            self.x = position_object.x
            self.y = position_object.y
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        return self

    def __str__(self):
        return "({}, {})".format(self.x, self.y)
