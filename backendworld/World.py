from Conf import Conf
import random
from Position import Position


#me doing this not anyone else
class World:
    def __init__(self):
        self.conf = Conf()
        self.conf.world = self
        self.age = 0
        self.tectonicBoundaries = set()
        self.tectonicPlates = set()
        self.tectonicCells = set()
        print("self conf {}".format(self.conf.class_for_name('GridStructure')))
        self._dataStructure = self.conf.class_for_name('GridStructure')(conf=self.conf)
        print("data structure type {}".format(self._dataStructure))
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
        for cell in self.tectonicCells:
            cell.step()

    def diverge(self, p1, p2, boundary):
        '''
        TODO
        :param p1: First plate
        :param p2: Second plate
        :param boundary: Boundary of p1 and p2
        :return:
        '''
        pass

    def converge(self, p1, p2, boundary):
        '''
        TODO
        :param p1: First plate
        :param p2: Second plate
        :param boundary: Boundary of p1 and p2
        :return:
        '''
        pass

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
        self._dataStructure.move_cell(random_cell, destination=random_position, relative=True)
        print("New info for random cell {}".format(random_cell))
        # self._dataStructure.move_cell(random_cell, relative=(relx,rely))

    def access_data_struct(self):
        '''
        Helper function
        :return: World._dataStructure
        '''
        return self._dataStructure
