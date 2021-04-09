from backendstorage.StorageMechanisms.ArrayStructure import ArrayStructure
from backendstorage.StorageMechanisms.TwoDimensionalArray import TwoDimensionalArray
from backendstorage.CustomExceptions import *
# from backendstorage.Vertices.VertexPoint import VertexPoint
from backendstorage.Cells.Cell import Cell
from Position import Position

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
        self.cellClassArgs = {'conf': self.conf, 'world_cell': 'TectonicCell', 'include_TwoDimensionalArray_pos': True}
        self.vertexClassName = 'VertexPoint'
        self.vertexClass = self.conf.class_for_name(self.vertexClassName)
        self.CellStorage = TwoDimensionalArray(rows=self.height, cols=self.width, createElem=self.cellClass, createElemKwargs = self.cellClassArgs)
        self.VertexStorage = TwoDimensionalArray(rows=self.height, cols=self.width, createElem=self.vertexClass)
        # self.width = self.CellStorage.cols
        # self.height = self.CellStorage.rows

    def print_contents(self):
        """
        Prints the stuff (cells/vertices) being stored
        :return:
        """
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
        """
        Subdivides every cell of the GridStructure into two both horizontally and vertically
        (for a total of four new cells in the place of every one original cell)
        :return:
        """
        # TODO: More documentation needed on attributes of newly created cells,
        #  such as what features are inherited and what's default initialized values

        # TODO: Subdivide vertices as well as columns
        #  (this may be handled when the to-do about relationships between cells and vertices is done)
        self.CellStorage.subdivide()
        self.width = self.CellStorage.cols
        self.height = self.CellStorage.rows

    def move_cell(self, cell: Cell, destination: Position, relative: bool = False):
        """
        Move a given cell to a position within GridStructure
        :param cell: Cell to be moved
        :param destination: Where the cell should be moved to
        :param relative: Whether the destination position is relative to the current position or absolute
        :return:
        """
        # TODO:
        #  Somewhere (not in this function, possibly not even in this class),
        #  there needs to be logic to wrap positions when moving cells

        # TODO: Somewhere, cell needs to change in world not just data storage
        #  use (make?) functions from (TectonicCell?) to change location within world coordinates
        old_position = cell.dataStoragePosition

        if relative is True:
            destination.change_position(cell.dataStoragePosition)
        print("cell to be moved: old position {} new position {}".format(old_position, destination))
        cell.ds_pos = destination
        self.CellStorage[destination.y][destination.x] = cell
        new_cellClassArgs = self.cellClassArgs.copy()
        if 'include_TwoDimensionalArray_pos' in self.cellClassArgs:
            new_cellClassArgs['ds_pos'] = old_position
        self.CellStorage[old_position.y][old_position.x] = self.cellClass(**new_cellClassArgs)
        print("Old cell {} moved to {}".format(cell, destination))
        print("New cell {} created at {}".format(self.CellStorage[old_position.y][old_position.x], old_position))
