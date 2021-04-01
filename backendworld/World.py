from Conf import Conf
import random

class World:
    def __init__(self):
        self.conf = Conf()
        self.conf.world = self
        self.age = 0
        self.tectonicBoundaries = set()
        self.tectonicPlates = set()
        self.tectonicCells = set()
        self._dataStructure = self.conf.class_for_name('GridStructure')(conf=self.conf)
        print("data structure type {}".format(self._dataStructure))
        self.images = {}
        self.annotatedImages = {}

    def step(self):
        self.age += 1
        for cell in self.tectonicCells:
            cell.age += 1

    def diverge(self, p1, p2, boundary):
        pass

    def converge(self, p1, p2, boundary):
        pass

    def random_wiggle(self):
        random_row = random.randint(0, self._dataStructure.height-1)
        random_col = random.randint(0, self._dataStructure.width-1)


        print("random row {}: {}".format(type(random_row),random_row))
        print("random col {}: {}".format(type(random_col),random_col))
        random_cell = self._dataStructure.lookupPosition(row=random_row, col=random_col)
        print("random cell {}: {}".format(type(random_cell),random_cell))
        relx = random.randint(-1,1)
        rely = random.randint(-1,1)
        self._dataStructure.move_cell(random_cell, relative=(relx,rely))

    def access_data_struct(self):
        return self._dataStructure
