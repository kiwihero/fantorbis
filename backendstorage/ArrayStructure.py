from backendstorage.GeneralStructure import *
from backendstorage.TwoDimensionalArray import TwoDimensionalArray

class ArrayStructure(GeneralStructure):
    def __init__(self, **kwargs):
        super(ArrayStructure, self).__init__(**kwargs)

    def print_contents(self):
        if type(self._ArrayStorage) is list:
            for row in self._ArrayStorage:
                print("row of len", len(row))
                printed_row = ''
                for col in row:
                    printed_row += str(col) + ' '
                print(printed_row)
        elif type(self._ArrayStorage) is TwoDimensionalArray:
            self._ArrayStorage.print_contents
        else:
            raise DoesNotExistError("ArrayStorage")

    def _lookup_position(self,row,col):
        return self._ArrayStorage[row][col]

    # def move_cell(self, cell, destination):

    def __iter__(self):
        if not type(self._ArrayStorage) is list:
            raise DoesNotExistError("ArrayStorage")
        return _GeneralArrayIterator(self._ArrayStorage, self)


class _GeneralArrayIterator(GeneralIterator):

    def __init__(self, grid, struct, **kwargs):
        self._grid = grid
        self.struct = struct
        print("self grid address {} grid address {}".format(hex(id(self._grid)),hex(id(grid))))
        self._index = [0, 0]
        super(_GeneralArrayIterator, self).__init__(**kwargs)

    def __next__(self):
        if self._index[0] < len(self._grid) and self._index[1] < len(
                self._grid[self._index[0]]):
            result = self._grid[self._index[0]][self._index[1]]
            print('\titr address {} {} \'if result\' {} from index {} of {}: {}'.format(hex(id(result)),hex(id(self._grid[self._index[0]][self._index[1]])),result, self._index, type(self._grid),self._grid))
            print("lookup result {} address {}".format(self.struct._lookup_position(self._index[0],self._index[1]),hex(id(self.struct._lookup_position(self._index[0],self._index[1])))))
            self._index[1] += 1
            return result
        elif self._index[0] + 1 < len(self._grid):
            self._index[0] += 1
            self._index[1] = 0
            result = self._grid[self._index[0]][self._index[1]]
            print('\titr address {} {} \'elif result\' {} from index {} of {}: {}'.format(hex(id(result)),hex(id(self._grid[self._index[0]][self._index[1]])),result, self._index, type(self._grid),self._grid))
            self._index[1] += 1
            return result
        raise StopIteration
