from backendworld.WorldAttribute import WorldAttribute
from Position import Position
from backendstorage.Vertices.Vertex import Vertex
from shapely.geometry import LineString, LinearRing, Polygon, Point, MultiPolygon
import geopandas as gpd
import pandas as pd
from backendworld.TectonicCell import TectonicCell
from shapely.ops import unary_union
import random

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
        self.add_tectonic_cell(cell['ShapelyCell'].world_cell)
        mini_cell_list = {'geometry':cell['geometry'],'ShapelyCell':cell['ShapelyCell']}
        print("mini cell list\n{}".format(mini_cell_list))
        print("mini cell area\n{}\nEnd mini cell area".format(cell['geometry'].area))
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
        series_data = {'ShapelyPlate':self, 'geometry':self.geometry, 'area':self.geometry.area, 'length':self.geometry.boundary.length}
        self.as_series = pd.Series(data=series_data, index=['geometry', 'ShapelyPlate','area','length'])
        print("plate area\n{}\nEnd plate area".format(series_data['geometry'].area))
        return self.series

    def add_tectonic_cell(self, cell: TectonicCell):
        self.tectonicCells.add(cell)

    def random_cell(self):
        if len(self.containing_cells) is 0:
            raise Exception("No Cells available, was plate initiated correctly?")
        random_number = random.randint(1,len(self.containing_cells))-1
        print("random number {} of len {}".format(random_number,len(self.containing_cells)))
        return self.containing_cells.iloc[random_number]


    def random_interior_boundary(self):
        print("finding interior boundary of plate with {} cells".format(len(self.containing_cells)))
        if len(self.containing_cells) > 1:
            random_row = self.random_cell()
            random_cell = random_row['ShapelyCell']
            # print("random cell {}".format(random_cell))
            # print("random cell world cell {}".format(random_cell.world_cell))
            cell_neighbors = self.world.access_data_struct().find_neighbors(random_row)
            cell_neighbors_shpcells = cell_neighbors.iloc[0]['ShapelyCell']
            # print("cell neighbors {}".format(cell_neighbors))
            # print("cell neighbors shpcells {}".format(cell_neighbors_shpcells))
            # print("cell neighbors shpcells world cell {}".format(cell_neighbors_shpcells.world_cell))
            # raise Exception
            # print("types {}, {}".format(type(random_cell), type(cell_neighbors_shpcells)))
            boundary_linestring = random_cell.polygon.exterior.intersection(cell_neighbors_shpcells.polygon.exterior)
            # print("boundary linestring {}".format(boundary_linestring))
            return (boundary_linestring,random_cell,cell_neighbors_shpcells)
            # print("valid")
        else:
            raise Exception("Cannot find an interior boundary of a plate without two cells to create an interior boundary")

    def __str__(self):
        return "Tectonic plate area {}, {} cells, bounds {}".format(self.series['area'],len(self.containing_cells),self.geometry.boundary)

