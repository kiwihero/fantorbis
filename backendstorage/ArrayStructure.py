from backendstorage.GeneralStructure import *

class ArrayStructure(GeneralStructure):
    def __init__(self, **kwargs):
        super(ArrayStructure, self).__init__(**kwargs)

    def print_contents(self):
        if not type(self._ArrayStorage) is list:
            raise DoesNotExistError("ArrayStorage")
        for row in self._ArrayStorage:
            print("row of len", len(row))
            printed_row = ''
            for col in row:
                printed_row += str(col) + ' '
            print(printed_row)

    # def move_cell(self, cell, destination):

    def __iter__(self):
        if not type(self._ArrayStorage) is list:
            raise DoesNotExistError("ArrayStorage")
        return _GeneralArrayIterator(self)


class _GeneralArrayIterator(GeneralIterator):

    def __init__(self, grid, **kwargs):
        self._grid = grid
        self._index = [0, 1]
        super(_GeneralArrayIterator, self).__init__(**kwargs)

    def __next__(self):
        if self._index[0] < len(self._grid.ArrayStorage) and self._index[1] < len(
                self._grid.ArrayStorage[self._index[0]]):
            result = self._grid.ArrayStorage[self._index[0]][self._index[1]]
            self._index[1] += 1
            return result
        elif self._index[0] + 1 < len(self._grid.ArrayStorage):
            self._index[0] += 1
            self._index[1] = 0
            result = self._grid.ArrayStorage[self._index[0]][self._index[1]]
            return result
        raise StopIteration
