from backendstorage.ArrayStructure import ArrayStructure
from backendstorage.TwoDimensionalArray import TwoDimensionalArray

class GridStructure(ArrayStructure):
    def __init__(self, width=2, height=2, **kwargs):
        super(GridStructure, self).__init__(**kwargs)
        self.cellShape = 'rectangle'
        self.cellClassName = 'GridCell'
        self.cellClassFile = 'backendstorage.GridCell'
        self.cellClass = self.conf.class_for_name(module_name=self.cellClassFile, class_name=self.cellClassName)
        self.width = width
        self.height = height
        self._ArrayStorage = TwoDimensionalArray(rows=self.height, cols=self.width, createElem=self.cellClass)

    def subdivide(self):
        self._ArrayStorage.subdivide()
        self.width = self._ArrayStorage.cols
        self.height = self._ArrayStorage.rows

    def subdivide_rows(self):
        self._ArrayStorage.subdivide_rows()

    def subdivide_cols(self):
        self._ArrayStorage.subdivide_cols()






