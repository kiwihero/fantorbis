from Conf import Conf
import random
from Position import Position
# from shapely.ops import snap
from shapely.ops import shared_paths, split
from shapely.geometry import MultiLineString

class World:
    def __init__(self):
        self.conf = Conf()
        self.conf.world = self
        self.age = 0
        self.tectonicBoundaries = set()
        self.tectonicPlates = set()
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
