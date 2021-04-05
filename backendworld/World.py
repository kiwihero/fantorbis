from Conf import Conf
import random
from Position import Position
from backendworld.WorldAction import random_wiggle_action

# TODO: THIS FILE NEEDS DOCSTRINGS
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
        self.conf.log_from_conf(level='info', message='World age {} step by one'.format(self.age))
        self.age += 1
        for cell in self.tectonicCells:
            cell.step()

    def diverge(self, p1, p2, boundary):
        pass

    def converge(self, p1, p2, boundary):
        pass

    def random_wiggle(self):
        return random_wiggle_action(self)

    def access_data_struct(self):
        return self._dataStructure
