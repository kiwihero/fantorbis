from backendworld.TectonicBoundary import *
from backendworld.TectonicPlate import *
from backendstorage.GridStructure import *

class World:
    def __init__(self):
        self.age = 0
        self.tectonicBoundaries = set()
        self.tectonicPlates = set()
        self.dataStructure = GridStructure()
        self.images = {}

    def step(self):
        self.age += 1

    def diverge(self, p1, p2, boundary):
        pass

    def converge(self, p1, p2, boundary):
        pass
