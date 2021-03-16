from backendstorage.TectonicBoundary import *
from backendstorage.TectonicPlate import *

class World:
    def __init__(self):
        self.age = 0
        self.tectonicBoundaries = set()
        self.tectonicPlates = set()

    def diverge(self, p1, p2, boundary):
        pass

    def converge(self, p1, p2, boundary):
        pass
