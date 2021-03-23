from backendstorage.Cell import Cell
class GridCell(Cell):
    def __init__(self, **kwargs):
        super(GridCell, self).__init__(**kwargs)

    def __copy__(self):
        return GridCell()

    def __deepcopy__(self, memodict={}):
        return GridCell()
