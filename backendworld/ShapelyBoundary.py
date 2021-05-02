from backendworld.WorldAttribute import WorldAttribute
from Position import Position
from backendstorage.Vertices.Vertex import Vertex
import geopandas as gpd
import pandas as pd
from backendworld.ShapelyPlate import TectonicPlate
from shapely.geometry import LineString, LinearRing
from shapely.ops import unary_union

class TectonicBoundary(WorldAttribute):
    """
        A boundary dividing TectonicPlates within a world
    """

    @property
    def bounds(self):
        return self.boundary_line.bounds

    @property
    def geometry(self):
        return self.boundary_line

    @property
    def boundary(self):
        return self.boundary_line

    def __init__(self, boundary=None, shp_cells=None, tectonic_plates=None, **kwargs):
        super(TectonicBoundary, self).__init__(**kwargs)

        if boundary is None:
            self.boundary_line = LineString()
            # self.boundary_linearring = LinearRing()
        else:
            self.boundary_line = LineString(boundary)
            # boundary_list = list(self.boundary_linestring.coords)
            # print("boundary list {}".format(boundary_list))
            # print("bourdary first {}".format(boundary_list[0]))
            # boundary_list.append(boundary_list[0])
            # print("boundary list {}".format(boundary_list))

            # self.boundary_linearring = LinearRing(boundary_list)#+[boundary_list[0]])
            # print("boundary ring {}".format(self.boundary_linearring))
            # raise Exception

        self.perimeter_shp_cells = gpd.GeoDataFrame(columns=['ShapelyCell', 'geometry', 'perpendicular_line'])
        if shp_cells is not None:
            for shp_cell in shp_cells:
                print("shp cell world cell",shp_cell.world_cell)
                # raise Exception
                if self.boundary_line is not None:
                    intersecting_boundary = shp_cell.polygon.exterior.intersection(self.boundary_line)
                    # print("intersecting boundary {}".format(intersecting_boundary))
                    parallel_boundary_left = intersecting_boundary.parallel_offset(intersecting_boundary.length,'left')
                    parallel_boundary_right = intersecting_boundary.parallel_offset(intersecting_boundary.length,'right')
                    # print("parallel left {}, right {}".format(parallel_boundary_left.boundary[1],parallel_boundary_right.boundary[0]))
                    perpendicular_boundary =LineString([parallel_boundary_left.boundary[1], parallel_boundary_right.boundary[0]])
                    perpendicular_boundary = perpendicular_boundary.intersection(shp_cell.polygon.exterior)
                else:
                    perpendicular_boundary = LineString()
                # print("perpendicular boundary",perpendicular_boundary)
                shp_cell_dict = {'ShapelyCell':shp_cell, 'geometry':shp_cell.polygon, 'perpendicular_line':perpendicular_boundary}
                shp_cell_ser = pd.Series(data=shp_cell_dict,index=['ShapelyCell', 'geometry', 'perpendicular_line'])
                self.perimeter_shp_cells = self.perimeter_shp_cells.append(shp_cell_ser, ignore_index=True)

        self.perimeter_plates = gpd.GeoDataFrame(columns=['TectonicPlate', 'geometry'])
        if tectonic_plates is not None:
            if type(tectonic_plates) is TectonicPlate:
                tectonic_plates = [tectonic_plates]
            for tec_plt in tectonic_plates:
                print("tectonic plate", tec_plt)
                tec_plt_dict = {'TectonicPlate':tec_plt, 'geometry':tec_plt.geometry}
                tec_plt_ser = pd.Series(data=tec_plt_dict,index=['TectonicPlate', 'geometry'])
                self.perimeter_plates = self.perimeter_plates.append(tec_plt_ser, ignore_index=True)

    def add_shp_cells(self, df):
        print("old linestring {}".format(self.boundary_line))
        # print("old linearring {}".format(self.boundary_linearring))
        print("old perimeter cells\n{}\nEnd old perimeter cells",self.perimeter_shp_cells)
        print("adding cells\n{}\nEnd adding cells".format(df))
        if type(df) is pd.Series:
            self.perimeter_shp_cells = self.perimeter_shp_cells.append(df,ignore_index=True)
        else:
            self.perimeter_shp_cells = self.perimeter_shp_cells.append(df)
        print("new perimeter cells\n{}\nEnd new perimeter cells".format(self.perimeter_shp_cells))
        combo = unary_union(self.perimeter_shp_cells['geometry'])
        print("combo type: {}, {}".format(type(combo),combo))
        self.boundary_line = combo.exterior
        print("boundary: {}, {}".format(type(self.boundary_line), self.boundary_line))
        # raise Exception

    def stretch_boundary(self):
        """
        Force a boundary to expand
        Cells along boundary gain velocity perpendicular to boundary, speed of once cell per step
        :return:
        """
        print("perimeter shp cells\n{}\nEnd perimeter shp cells".format(self.perimeter_shp_cells))
        # for x in range(len(self.perimeter_shp_cells)):
        #     shp_cell = self.perimeter_shp_cells.iloc[x]
        #     # print("\nshp cell\n{}\nEnd shp cell\n".format(shp_cell))
        #     print("world cells")
        #     print(shp_cell['ShapelyCell'].world_cell,shp_cell['ShapelyCell'].world_cell.world)
        #     # self.world.access_data_struct().move_cell(cell=shp_cell['ShapelyCell'], velocity=shp_cell['perpendicular_line'])
        # raise Exception

        lambda_results = self.perimeter_shp_cells.apply(lambda x: self.world.access_data_struct().move_cell(cell=x['ShapelyCell'],velocity=x['perpendicular_line'], allow_update=False), axis=1)
        lambda_results = lambda_results.dropna(how='all')
        print("lambda results\n{}\nend lambda results".format(lambda_results))
        # lambda_results = lambda_results.loc[lambda_results['ShapelyCell'] != False]
        # print("lambda results\n{}\nend lambda results".format(lambda_results))
        self.add_shp_cells(lambda_results)
        # raise Exception
        print(lambda_results['ShapelyCell'])
        print("data struct\n{}\nend data struct".format(self.world.access_data_struct()))
        self.world.access_data_struct().update_cells()
        print("after update data struct\n{}\nend after update data struct".format(self.world.access_data_struct()))

        print("after update data struct hghts\n{}\nend after update data structhghts".format(self.world.access_data_struct().CellStorage['stack_size']))
        # raise Exception

        # for x in range(len(self.perimeter_shp_cells)):
        #     shp_cell = self.perimeter_shp_cells.iloc[x]
        #     print("\nshp cell\n{}\nEnd shp cell\n".format(shp_cell))
        #     self.world.access_data_struct().move_cell(
        #         cell=shp_cell['ShapelyCell'],velocity=shp_cell['perpendicular_line'])

