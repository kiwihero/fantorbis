from backendstorage.CustomExceptions import *
# # All of the structures inherit this
# # Declares some methods expected, default to returning an error when those are called and not implemented in inherited
class GeneralStructure:
    """
    This is NOT an actual structure, do not create instances of this
    """
    def __init__(self, conf=None, **kwargs):
        self.cellShape = None
        self.conf = conf