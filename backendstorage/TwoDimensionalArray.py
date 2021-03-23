class TwoDimensionalArray:
    def __init__(self, rows=0, cols=0, defaultElem=None, createElem=None):
        self.array = []
        self.rows = rows
        self.cols = cols
        self.defaultElem = defaultElem
        while(self.rows > len(self.array)):
            row = []
            for c in range(self.cols):
                if createElem != None:
                    elem = createElem()
                    row.append(elem)
                else:
                    row.append(self.defaultElem)
            self.array.append(row)

    def __iter__(self):
        return _TwoDimensionalArrayIterator(self.array)

    def lookupPosition(self,row,col):
        return self.array[row][col]

    def __getitem__(self, item):
        return self.array[item]

    def print_contents(self):
        if type(self.array) is list:
            for row in self.array:
                print("row of len", len(row))
                printed_row = ''
                for col in row:
                    printed_row += str(col) + ' '
                print(printed_row)



class _TwoDimensionalArrayIterator:
    def __init__(self, grid, **kwargs):
        self._grid = grid
        self._index = [0, 0]

    def __next__(self):
        if self._index[0] < len(self._grid) and self._index[1] < len(self._grid[self._index[0]]):
            result = self._grid[self._index[0]][self._index[1]]
            self._index[1] += 1
            return result
        elif self._index[0] + 1 < len(self._grid):
            self._index[0] += 1
            self._index[1] = 0
            result = self._grid[self._index[0]][self._index[1]]
            self._index[1] += 1
            return result
        raise StopIteration