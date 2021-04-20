import geopandas as gpd

from backendstorage.StorageMechanisms.ArrayStructure import *


class ShapelyStructure(ArrayStructure):
    """
    Not a real structure either, don't use this itself
    Structures that use arrays instead of pointers to hold information
    """
    def __init__(self, **kwargs):
        """
        This is an actual structure
        :param kwargs:
        """
        super(ShapelyStructure, self).__init__(**kwargs)
        self.CellStorage = gpd.GeoDataFrame(columns=['Name', 'Age'])
