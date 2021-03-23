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
        print("array storage", self._ArrayStorage)
        print("array item", self._ArrayStorage[1][1])





