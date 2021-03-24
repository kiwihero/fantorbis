from backendstorage.Cell import Cell
import copy
class GridCell(Cell):
    def __init__(self, parent=None, **kwargs):
        super(GridCell, self).__init__(**kwargs)
        self.parent = parent

    def __copy__(self):
        newCell = GridCell(parent=self.parent)
        return newCell