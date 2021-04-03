from backendstorage.StorageMechanisms.ArrayStructure import ArrayStructure
from backendstorage.StorageMechanisms.TwoDimensionalArray import TwoDimensionalArray
from backendstorage.CustomExceptions import *
# from backendstorage.Vertices.VertexPoint import VertexPoint
#
class GridStructure(ArrayStructure):
    def __init__(self, width=2, height=2, **kwargs):
        """
        This is an actual storage class
        Info is stored in a grid-style array
        :param width: The width of the array (x), defaults to 2
        :param height: The height of the array (y), defaults to 2
        :param kwargs:
        """
        super(GridStructure, self).__init__(**kwargs)
        self.width = width
        self.height = height

        self.cellShape = 'rectangle'

        # --------------------------------------------------------------------------------------------------------------
        # Ability to create other classes from strings
        # --------------------------------------------------------------------------------------------------------------

        self.cellClassName = 'Cell'
        self.cellClass = self.conf.class_for_name(self.cellClassName)
        self.cellClassArgs = {'conf': self.conf, 'world_cell': 'TectonicCell'}
        self.vertexClassName = 'VertexPoint'
        self.vertexClass = self.conf.class_for_name(self.vertexClassName)
        self.CellStorage = TwoDimensionalArray(rows=self.height, cols=self.width, createElem=self.cellClass, createElemKwargs = self.cellClassArgs)
        self.VertexStorage = TwoDimensionalArray(rows=self.height, cols=self.width, createElem=self.vertexClass)

    def print_contents(self):
        print("Printing as array structure")
        if type(self.CellStorage) is list:
            for row in self.CellStorage:
                print("row of len", len(row))
                printed_row = ''
                for col in row:
                    printed_row += str(col) + ' '
                print(printed_row)
        elif type(self.CellStorage) is TwoDimensionalArray:
            self.CellStorage.print_contents()
        else:
            print("what did you try to print?")
            raise DoesNotExistError("ArrayStorage")

    def subdivide(self):
        self.CellStorage.subdivide()

    def move_cell(self, cell, destination=None, relative=None):
        # TODO: Functionality to move cell:
        #  use functions from TwoDimensionalArray to change storage location (self.CellStorage),
        #  use (make?) functions from (TectonicCell?) to change location within world coordinates
        pass
