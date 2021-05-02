from Conf import Conf
import random
from Position import Position
# from shapely.ops import snap
from shapely.ops import shared_paths, split
from shapely.geometry import MultiLineString
from backendworld.ShapelyPlate import TectonicPlate
from backendworld.ShapelyBoundary import TectonicBoundary
import geopandas as gpd
import pandas as pd

class World:
    def __init__(self):
        self.conf = Conf()
        self.conf.world = self
        self.age = 0
        self.tectonicBoundaries = set()
        self.tectonicBoundariesDf = gpd.GeoDataFrame(columns=['geometry','ShapelyBoundary'])
        self.tectonicPlates = set()
        self.tectonicPlatesDf = gpd.GeoDataFrame(columns=['geometry', 'ShapelyPlate','area','length'])
        self.tectonicCells = set()
        self._dataStructure = self.conf.class_for_name('ShapelyStructure')(conf=self.conf)
        self.images = {}
        self.annotatedImages = {}
        self.detailedImages = {}

    def step(self):
        '''
        A single step in time
        :return:
        '''
        self.conf.log_from_conf(level='info', message='World age {} step by one'.format(self.age))
        self.age += 1
        print("When stepping world to age {}, know of {} tectonic cells".format(self.age,len(self.tectonicCells)))
        # for cell in self.tectonicCells.copy():
        for cell in self.tectonicCells.copy():
            cell.step()
        self._dataStructure.step_move()

    def diverge(self, p1, p2, boundary):
        '''
        TODO: Divergence
        :param p1: First plate
        :param p2: Second plate
        :param boundary: Boundary of p1 and p2
        :return:
        '''
        forward, backward = shared_paths(p1,p2)
        shared_bound = MultiLineString(forward,backward)
        split_p1_bound = split(p1.boundary,shared_bound)
        split_p2_bound = split(p2.boundary,shared_bound)
        split_p1_bound = split_p1_bound.difference(shared_bound)
        split_p2_bound = split_p2_bound.difference(shared_bound)

        pass

    def converge(self, p1, p2, boundary):
        '''
        TODO: Convergence
        :param p1: First plate
        :param p2: Second plate
        :param boundary: Boundary of p1 and p2
        :return:
        '''
        overlap = p1.intersection(p2)

    def converge_cells(self, t1, t2):
        print("converging cells into {}".format(t1))
        try:
            iter(t2)
            t1.stack_size += len(t2)
            new_ages = []
            new_velocities = []
            new_heights = []
            total = 1
            for t in t2:
                new_ages.append(t.age)
                new_velocities.append(t.velocity)
                new_heights.append(t.height)
                total += 1

            t1.age = (t1.age + sum(new_ages)) / total
            t1.velocity = t1.velocity.average(new_velocities)
            t1.height = (t1.height + sum(new_heights))/total
            t2 = t1
            print("done converging cells into {}".format(t1))
            return t1
        except TypeError:
            return self.converge_cells(t1,[t2])



    def random_wiggle(self):
        '''
        Wiggle a random cell one step
        Testing function, not for production use
        :return:
        '''
        random_row = random.randint(0, self._dataStructure.height-1)
        random_col = random.randint(0, self._dataStructure.width-1)
        print("world data structure {} type {} height {} type {} id {}".format(self._dataStructure, type(self._dataStructure), self._dataStructure.height, type(self._dataStructure.height), hex(id(self._dataStructure.height))))


        print("random row {}: {} max {}".format(type(random_row),random_row,self._dataStructure.height-1))
        print("random col {}: {}".format(type(random_col),random_col))
        random_cell = self._dataStructure.CellStorage[random_row][random_col]
        print("random cell {}: {}".format(type(random_cell),random_cell))
        relx = random.randint(-1,1)
        rely = random.randint(-1,1)
        random_position = Position(relx, rely)
        print("Moving random cell to {}".format(random_position))
        self._dataStructure.move_cell(random_cell, destination=random_position, relative=True, change_velocity=True)
        # raise Exception
        print("New info for random cell {}".format(random_cell))
        # self._dataStructure.move_cell(random_cell, relative=(relx,rely))

    def access_data_struct(self):
        '''
        Helper function
        :return: World._dataStructure
        '''
        return self._dataStructure

    def new_tectonic_plate(self, inp):
        print("New tectonic plate input type {}".format(type(inp)))
        if type(inp) is gpd.GeoDataFrame:
            plate = TectonicPlate(world=self)
            self.tectonicPlates.add(plate)
            plate_cells = plate.add_struct_cell(inp)
            # print("plate cells\n{}\nend plate cells".format(plate_cells))
            self.tectonicPlatesDf = self.tectonicPlatesDf.append(plate_cells, ignore_index=True)
            # print("tectonic plates df\n{}\nEnd tectonic plates df".format(self.tectonicPlatesDf))

            # raise Exception
            return plate

        raise Exception("You need to specify an argument for new_tectonic_plate")

    def clear_tectonic_plates(self):
        self.tectonicPlates = set()
        self.tectonicPlatesDf = gpd.GeoDataFrame(columns=['geometry', 'ShapelyPlate','area','length'])

    def _random_plate(self):
        """
        Internal function to get a random plate
        :return:
        """
        if len(self.tectonicPlates) is 0:
            raise Exception("No plates available, was world initiated correctly?")
        random_number = random.randint(1,len(self.tectonicPlates))-1
        return list(self.tectonicPlates)[random_number]


    def force_split(self, plate=None, boundary=None):
        """
        Forces a split (divergent boundary)
        :param plate: Can specify a plate to be split
        :param boundary: Can specify a plate boundary to split along
        :return:
        """
        if plate is None and boundary is None:
            print("available plates\n{}\nEnd available plates".format(self.tectonicPlates))
            for plate in self.tectonicPlates:
                print("\tPlate {}".format(str(plate)))
            valid_plate = False
            counter = 0
            while valid_plate == False and counter < 2*len(self.tectonicPlates):
                plate = self._random_plate()
                print("plate to create split {}".format(plate))
                boundary_tuple = plate.random_interior_boundary()
                counter += 1
                if boundary_tuple is not None:
                    valid_plate = True
            boundary = boundary_tuple[0]
            boundary_cell1 = boundary_tuple[1]
            boundary_cell2 = boundary_tuple[2]
            removed = plate.remove_struct_cell([boundary_cell1,boundary_cell2])
            new_plate = self.new_tectonic_plate(removed)
            print("New tectonic plate\n{}\nEnd new tectonic plate".format(new_plate))
            # raise Exception
            # print("Boundary to split {}".format(boundary))
            print("Cells for boundary {}, {}".format(str(boundary_cell1),str(boundary_cell2)))
            # print("Cells for boundary {}, {}".format(str(boundary_cell1.world_cell.world),str(boundary_cell2.world_cell.world)))
            # raise Exception
            tectonic_boundary = TectonicBoundary(world=self, boundary=boundary, shp_cells=(boundary_cell1,boundary_cell2), tectonic_plates=(plate,new_plate))
            print("tectonic boundary {}".format(tectonic_boundary))
            # raise Exception
            tectonic_boundary_dict = {'geometry': tectonic_boundary.geometry, 'ShapelyBoundary':tectonic_boundary}
            tectonic_boundary_series = pd.Series(data=tectonic_boundary_dict,index=['geometry', 'ShapelyBoundary'])
            print("new boundaries series\n{}\nEnd boundaries series".format(tectonic_boundary_series))
            # raise Exception
            self.tectonicBoundariesDf = self.tectonicBoundariesDf.append(tectonic_boundary_series,ignore_index=True)
            print("boundaries df {}".format(self.tectonicBoundariesDf['geometry']))

            tectonic_boundary.stretch_boundary()
            print("boundaries df\n{}\nEnd boundaries df".format(self.tectonicBoundariesDf))
            self.update_tectonic_boundaries()
            print("boundaries df\n{}\nEnd boundaries df".format(self.tectonicBoundariesDf))
            # raise Exception


        # if plate is None and boundary is None:

    def update_tectonic_boundaries(self):
        lambda_results = self.tectonicBoundariesDf
        print("lambda results\n{}\nend lambda results".format(lambda_results))
        lambda_results['geometry'] = self.tectonicBoundariesDf.apply(lambda x: x['ShapelyBoundary'].geometry, axis=1)
        print("lambda results\n{}\nend lambda results".format(lambda_results))
        self.tectonicBoundariesDf = lambda_results
        # raise Exception
        # self.tectonicBoundariesDf = gpd.GeoDataFrame(columns=['geometry','ShapelyBoundary'])

        # lambda_results = df.apply(lambda x: self.strip_struct_cell(x), axis=1)


