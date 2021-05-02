from backendworld.WorldAttribute import WorldAttribute
from Position import Position
from backendstorage.Vertices.Vertex import Vertex
from shapely.geometry import LineString, LinearRing, Polygon, Point, MultiPolygon
import geopandas as gpd
import pandas as pd
from backendworld.TectonicCell import TectonicCell
from shapely.ops import unary_union
import random
# from backendstorage.Cells.ShapelyCell import ShapelyCell

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

    def strip_struct_cell(self, cell, add: bool = False, remove: bool = False):
        if add is True:
            self.add_tectonic_cell(cell['ShapelyCell'].world_cell)
        if remove is True:
            self.remove_tectonic_cell(cell['ShapelyCell'].world_cell)
        mini_cell_list = {'geometry':cell['geometry'],'ShapelyCell':cell['ShapelyCell']}
        print("mini cell list\n{}".format(mini_cell_list))
        print("mini cell area\n{}\nEnd mini cell area".format(cell['geometry'].area))
        mini_cell = pd.Series(data=mini_cell_list,index=['geometry', 'ShapelyCell'])
        # print("mini cell\n{}".format(mini_cell))
        return mini_cell

    def add_struct_cell(self, inp):
        if type(inp) is list:
            for elem in inp:
                self.add_struct_cell(elem)
            raise Exception("Not finished implementation")
        if type(inp) is gpd.GeoDataFrame:
            lambda_results = inp.apply(lambda x: self.strip_struct_cell(x, add=True), axis=1)
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
        raise Exception("Unknown input type")

    def add_tectonic_cell(self, cell: TectonicCell):
        self.tectonicCells.add(cell)

    def remove_struct_cell(self, inp):
        if type(inp) is gpd.GeoDataFrame:
            raise Exception("Removal not implemented for data frames")
            # lambda_results = df.apply(lambda x: self.strip_struct_cell(x), axis=1)
            # print("lambda results\n{}\nend lambda results".format(lambda_results))
        if type(inp) is list:
            print("Containing cells before drop\n{}\nend containing cells".format(self.containing_cells))
            removed_cells = gpd.GeoDataFrame(columns=['ShapelyCell', 'geometry'])
            for elem in inp:
                print("Cell to remove\n{}\nend cell to remove".format(elem))
                rem = self.remove_struct_cell(elem)
                print("rem\n{}\nend rem".format(rem))
                removed_cells = removed_cells.append(rem)
            print("Containing cells after drop\n{}\nend containing cells".format(self.containing_cells))
            print("Removed cells {}\n{}\nend removed cells".format(type(removed_cells),removed_cells))
            return removed_cells
            # raise Exception
        else:
            # matching_rows = containing_structure.loc[containing_structure['pos_point'] == self.centroid]

            matching_rows = self.containing_cells.loc[self.containing_cells['ShapelyCell'] == inp]
            print("matching rows {}\n{}\nend matching rows".format(type(matching_rows),matching_rows))
            removed_tectonic_df = matching_rows.apply(lambda x: self.remove_tectonic_cell(x), axis=1)
            # raise Exception
            self.containing_cells = self.containing_cells.loc[self.containing_cells['ShapelyCell'] != inp]
            print("matching rows\n{}\nend matching rows".format(matching_rows))
            return matching_rows

            # print("Matching rows\n{}\nend matching rows".format(matching_rows))
            # print("Containing cells before drop\n{}\nend containing cells".format(self.containing_cells))
            # self.containing_cells = self.containing_cells.drop(matching_rows)
            # print("Containing cells after drop\n{}\nend containing cells".format(self.containing_cells))

            # raise Exception


    def remove_tectonic_cell(self, inp):
        print("remove tectonic cell input type {}".format(type(inp)))
        if type(inp) is pd.Series:
            world_cell = inp['ShapelyCell'].world_cell
            print("world cell {}".format(world_cell))
            if world_cell not in self.tectonicCells:
                print("Cannot remove tectonic cell {} as it is no longer in the set of this plate".format(world_cell))
                return world_cell
            self.tectonicCells.remove(world_cell)
            return world_cell
        raise Exception("Unsure how to remove tectonic cell from input type {}".format(inp))


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
            print("Cannot find an interior boundary of a plate without two cells to create an interior boundary")
            return None


    def __str__(self):
        return "Tectonic plate area {}, {} cells, bounds {}".format(self.series['area'],len(self.containing_cells),self.geometry.boundary)

