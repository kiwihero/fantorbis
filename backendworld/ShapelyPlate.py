from backendworld.WorldAttribute import WorldAttribute
from Position import Position
from backendstorage.Vertices.Vertex import Vertex
from shapely.geometry import LineString, LinearRing, Polygon, Point, MultiPolygon
import geopandas as gpd
import pandas as pd
from backendworld.TectonicCell import TectonicCell
from shapely.ops import unary_union

class TectonicPlate(WorldAttribute):
    """
        A boundary dividing TectonicPlates within a world
    """
    @property
    def series(self):
        return self.as_series

    def __init__(self, **kwargs):
        self.plate_boundary = LinearRing()
        self.containing_cells = gpd.GeoDataFrame(columns=['ShapelyCell','geometry'])
        self.tectonicCells = set()
        self.geometry = MultiPolygon()
        self.as_series = pd.Series()
        super(TectonicPlate, self).__init__(**kwargs)

    def strip_struct_cell(self, cell):
        mini_cell_list = {'geometry':cell['geometry'],'ShapelyCell':cell['ShapelyCell']}
        # print("mini cell list\n{}".format(mini_cell_list))
        mini_cell = pd.Series(data=mini_cell_list,index=['geometry', 'ShapelyCell'])
        # print("mini cell\n{}".format(mini_cell))
        return mini_cell

    def add_struct_cell(self, df: gpd.GeoDataFrame):
        lambda_results = df.apply(lambda x: self.strip_struct_cell(x), axis=1)
        # print("lambda results\n{}\nend lambda results".format(lambda_results))
        self.containing_cells = self.containing_cells.append(lambda_results)
        # print("containing cells\n{}\nend containing cells".format(self.containing_cells))
        self.geometry = unary_union(self.containing_cells['geometry'])
        # print("New geometry\n{}\nend new geometry".format(self.geometry))
        # raise Exception
        series_data = {'ShapelyPlate':self, 'geometry':self.geometry}
        self.as_series = pd.Series(data=series_data, index=['geometry', 'ShapelyPlate'])
        return self.series

    def add_tectonic_cell(self, cell: TectonicCell):
        self.tectonicCells.add(cell)

