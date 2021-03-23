from backendstorage.ArrayStructure import ArrayStructure

class GridStructure(ArrayStructure):
    def __init__(self, width=2, height=2, **kwargs):
        super(GridStructure, self).__init__(**kwargs)
        self.cellShape = 'rectangle'
        self.width = width
        self.height = height
        self._ArrayStorage = [[None] * self.width] * self.height




