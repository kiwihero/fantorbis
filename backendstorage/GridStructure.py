from backendstorage.ArrayStructure import ArrayStructure
from backendstorage.TwoDimensionalArray import TwoDimensionalArray
from backendstorage.VertexPoint import VertexPoint

class GridStructure(ArrayStructure):
    def __init__(self, width=2, height=2, **kwargs):
        super(GridStructure, self).__init__(**kwargs)
        self.cellShape = 'rectangle'
        self.cellClassName = 'GridCell'
        self.cellClassFile = 'backendstorage.GridCell'
        self.cellChildName = self.conf.cellClass
        self.cellChildFile = self.conf.cellModule
        self.cellChildClass = self.conf.class_for_name(module_name=self.cellChildFile, class_name=self.cellChildName)
        self.cellClassArgs = {'conf':self.conf, 'childClass':self.cellChildClass}
        self.cellClass = self.conf.class_for_name(module_name=self.cellClassFile, class_name=self.cellClassName)
        self.vertexClassName = 'VertexPoint'
        self.vertexClassFile = 'backendstorage.VertexPoint'
        self.vertexClass = self.conf.class_for_name(module_name=self.vertexClassFile, class_name=self.vertexClassName)
        self.width = width
        self.height = height
        self._ArrayStorage = TwoDimensionalArray(rows=self.height, cols=self.width, createElem=self.cellClass, elemKwargs=self.cellClassArgs)
        self._VertexArrayStorage = TwoDimensionalArray(rows=self.height, cols=self.width, createElem=self.vertexClass)

    def subdivide(self):
        self._ArrayStorage.subdivide()
        self.width = self._ArrayStorage.cols
        self.height = self._ArrayStorage.rows

    def subdivide_rows(self):
        self._ArrayStorage.subdivide_rows()

    def subdivide_cols(self):
        self._ArrayStorage.subdivide_cols()

    def swap_cells(self, cell1, cell2):
        cell1pos = self._ArrayStorage.search_for_address(cell=cell1)
        cell2pos = self._ArrayStorage.search_for_address(cell=cell2)
        self._ArrayStorage.swap_pos(originRow=cell1pos['row'],originCol=cell1pos['col'],destRow=cell2pos['row'], destCol=cell2pos['col'])

    def move_cell(self, cell, destination=None, relative=None):
        if destination==None and relative==None:
            self.conf.log_from_conf('error', 'No destination or relative movement known to move cell')
            return
        cellpos = self._ArrayStorage.search_for_address(cell=cell)
        print("moving cell {}".format(cell))
        if destination == None:
            destination = [cellpos['row']+relative[0], cellpos['col']+relative[1]]

        print("Moving from {} to {}".format(cellpos, destination))

        self._ArrayStorage.move_pos(cellpos['row'], cellpos['col'], destination[0], destination[1])

    def search_for_cell(self, cell):
        return self._ArrayStorage.search_for_cell(cell)

    def lookupPosition(self,row,col):
        return self._ArrayStorage.lookupPosition(row=row, col=col)




