class Position:
    """
    The position functionality
    """
    def __init__(self):
        self.x = 0
        self.y = 0

    def change_position(self, position_object=None, x=0, y=0):
        if position_object is not None:
            self.x += position_object.x
            self.y += position_object.y
        else:
            self.x += x
            self.y += y

    def set_position(self, position_object=None, x=None, y=None):
        if position_object is not None:
            self.x = position_object.x
            self.y = position_object.y
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
