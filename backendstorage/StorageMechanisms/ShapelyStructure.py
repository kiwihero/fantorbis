import geopandas as gpd
import math

from backendstorage.StorageMechanisms.ArrayStructure import *
from backendstorage.Cells.ShapelyCell import ShapelyCell


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
        first_cell = ShapelyCell(
            conf=self.conf,
            shell=[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]],
            # shell=[[0, 0], [0, 1], [math.sqrt(3)/2, .5], [0, 0]],
            world_cell_args=dict([('world', self.conf.world)]),
            world_cell='TectonicCell'
        )
        self.CellStorage = gpd.GeoDataFrame(
            [[
                first_cell,
                first_cell.world_cell,
                first_cell,
                first_cell.centroid.x*first_cell.centroid.y
            ]],
            columns=['ShapelyCell', 'TectonicCell', 'geometry', 'pos']
        )


    def add_cell(self, shp_cell: ShapelyCell):
        """
        Add a ShapelyCell to the ShapelyStructure
        :param shp_cell:
        :return:
        """
        self.CellStorage = self.CellStorage.append({
            'TectonicCell': shp_cell.world_cell,
            'ShapelyCell': shp_cell,
            'geometry': shp_cell._geom()
        })

    def subdivide(self):
        """
        Subdivides every cell of the GridStructure into two both horizontally and vertically
        (for a total of four new cells in the place of every one original cell)
        :return:
        """
        n = [x.subdivide() for x in self.CellStorage['ShapelyCell']]
        self.CellStorage = gpd.GeoDataFrame(columns=['ShapelyCell', 'TectonicCell','geometry','pos'])
        for m in n:
            print("m",len(m),m)
            self.CellStorage = self.CellStorage.append(m)
            print(self.CellStorage['ShapelyCell'])


    def __str__(self):
        return str(self.CellStorage)
