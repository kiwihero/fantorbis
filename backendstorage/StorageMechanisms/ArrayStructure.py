from backendstorage.StorageMechanisms.GeneralStructure import *
from backendstorage.StorageMechanisms.TwoDimensionalArray import TwoDimensionalArray
#
class ArrayStructure(GeneralStructure):
    """
    Not a real structure either, don't use this itself
    Structures that use arrays instead of pointers to hold information
    """
    def __init__(self, **kwargs):
        super(ArrayStructure, self).__init__(**kwargs)