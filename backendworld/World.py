from backendworld.TectonicBoundary import *
from backendworld.TectonicPlate import *
from backendstorage.GridStructure import *
from Conf import Conf

class World:
    def __init__(self):
        self.conf = Conf()
        self.age = 0
        self.tectonicBoundaries = set()
        self.tectonicPlates = set()
        self.dataStructure = self.conf.class_for_name(self.conf.structureModule,self.conf.structureClass)()
        self.images = {}
        self.annotatedImages = {}

    def step(self):
        self.age += 1

    def diverge(self, p1, p2, boundary):
        pass

    def converge(self, p1, p2, boundary):
        pass
