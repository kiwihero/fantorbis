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
        # self.cellClassName = 'GridCell'
        self.cellClassName = 'Cell'
        self.cellClass = self.conf.class_for_name(self.cellClassName)
        self.vertexClassName = 'VertexPoint'
        self.vertexClass = self.conf.class_for_name(self.vertexClassName)
        self.CellStorage = TwoDimensionalArray(rows=self.height, cols=self.width, createElem=self.cellClass)
        self.VertexStorage = TwoDimensionalArray(rows=self.height, cols=self.width, createElem=self.vertexClass)
#         self.cellClassFile = 'backendstorage.GridCell'
#         self.cellChildName = self.conf.cellClass
#         self.cellChildFile = self.conf.cellModule
#         self.cellChildClass = self.conf.class_for_name(module_name=self.cellChildFile, class_name=self.cellChildName)
#         self.cellClassArgs = {'conf':self.conf, 'childClass':self.cellChildClass}
#         self.cellClass = self.conf.class_for_name(module_name=self.cellClassFile, class_name=self.cellClassName)
#         self.vertexClassName = 'VertexPoint'
#         self.vertexClassFile = 'backendstorage.VertexPoint'
#         self.vertexClass = self.conf.class_for_name(module_name=self.vertexClassFile, class_name=self.vertexClassName)
#
        # self._CellArrayStorage = TwoDimensionalArray(rows=self.height, cols=self.width, createElem=self.cellClass, elemKwargs=self.cellClassArgs)
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
#         self.width = self._CellArrayStorage.cols
#         self.height = self._CellArrayStorage.rows
#
#     def subdivide_rows(self):
#         self._CellArrayStorage.subdivide_rows()
#         self._VertexArrayStorage.subdivide_rows()
#
#     def subdivide_cols(self):
#         self._CellArrayStorage.subdivide_cols()
#         self._VertexArrayStorage.subdivide_cols()
#     #
#     # def swap_cells(self, cell1, cell2):
#     #     cell1pos = self._CellArrayStorage.search_for_address(cell=cell1)
#     #     cell2pos = self._CellArrayStorage.search_for_address(cell=cell2)
#     #     self._ArrayStorage.swap_pos(originRow=cell1pos['row'],originCol=cell1pos['col'],destRow=cell2pos['row'], destCol=cell2pos['col'])
#     #
#     def move_cell(self, cell, destination=None, relative=None):
#         if destination==None and relative==None:
#             self.conf.log_from_conf('error', 'No destination or relative movement known to move cell')
#             return
#
#         cellpos = cell.dataStoragePosition
#         print("moving cell {}: pos".format(cell,cellpos))
#         if destination == None:
#             destination = [cellpos['row']+relative[0], cellpos['col']+relative[1]]
#
#         print("Moving from {} to {}".format(cellpos, destination))
#
#         cell.move(newDataStoragePosition=destination, newWorldPosition=destination)
#
#         self._CellArrayStorage.move_pos(cellpos['row'], cellpos['col'], destination[0], destination[1])
#
#     # def search_for_cell(self, cell):
#     #     return self._CellArrayStorage.search_for_cell(cell)
#     #
#     def lookupPosition(self,row,col):
#         return self._CellArrayStorage.lookupPosition(row=row, col=col)
#
#     def resetVertices(self):
#         for cell in self._CellArrayStorage:
#             print(cell)
#
#
#
#
