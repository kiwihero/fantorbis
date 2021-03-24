import copy
class TwoDimensionalArray(list):
    def __init__(self, rows=0, cols=0, defaultElem=None, createElem=None, **kwargs):
        super(TwoDimensionalArray, self).__init__(**kwargs)
        self.array = []
        self.rows = rows
        self.cols = cols
        self.defaultElem = defaultElem
        self.createElem = createElem
        while(self.rows > len(self.array)):
            row = []
            for c in range(self.cols):
                if self.createElem != None:
                    elem = self.createElem()
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
            print("Printing contents of {} x {} array".format(self.rows,self.cols))
            for row in self.array:
                # print("row of len", len(row))
                printed_row = ''
                for col in row:
                    printed_row += str(col) + ' '
                print(printed_row)
        else:
            print("Oops! Array {} not correct type {}".format(self.array, type(self.array)))

    def search_for_cell(self,cell):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.lookupPosition(row=row,col=col) == cell:
                    return {'row': row, 'col': col}

    def search_for_attributes(self,attrDict):

        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.lookupPosition(row=row,col=col)
                match=True
                for attr, val in attrDict.items():
                    if cell.attr != val:
                        match=False
                        break #If one attribute doesn't work, stop comparing attributes: gets back to for loop going through the array
                if match == True:
                    return {'row': row, 'col': col}

    def search_for_address(self,address=None,cell=None):
        if address == None:
            if cell != None:
                address = hex(id(cell))
            else:
                return Exception
        for row in range(self.rows):
            for col in range(self.cols):
                if hex(id(self.lookupPosition(row=row,col=col))) == address:
                    return {'row': row, 'col': col}

    def swap_pos(self, originRow, originCol, destRow, destCol):
        temp_cell = self.remove_pos(originRow,originCol)
        self.move_pos(destRow,destCol,originRow,originCol)
        self.add_pos(temp_cell, destRow, destCol)


    def move_pos(self, originRow, originCol, destRow, destCol):
        cell = self.lookupPosition(row=originRow,col=originCol)
        self.add_pos(cell, destRow, destCol)

    def add_pos(self, cell, row, col):
        self.array[row][col] = cell

    def remove_pos(self, row, col):
        cell = self.lookupPosition(row,col)
        if self.createElem != None:
            self.array[row][col] = self.createElem()
        else:
            self.array[row][col] = self.defaultElem
        return cell

    def subdivide(self):
        self.subdivide_rows()
        self.subdivide_cols()
        print("size now rows {}, cols {}".format(self.rows,self.cols))

    def subdivide_rows(self):
        new_array = []
        for row in range(self.rows):
            new_row = []
            for col in range(self.cols):
                old_cell = self.array[row][col]
                # print("CELL TYPE {}".format(type(old_cell)))
                new_cell = copy.deepcopy(old_cell)
                # new_cell = old_cell.copy()
                new_row.append(new_cell)
            new_array.append(self.array[row])
            new_array.append(new_row)
        self.array = new_array
        self.rows = 2 * self.rows



    def subdivide_cols(self):
        new_array = []
        for row in range(self.rows):
            new_row = []
            for col in range(self.cols):
                cell = self.array[row][col]
                new_cell = copy.copy(cell)
                new_row.append(cell)
                new_row.append(new_cell)
            new_array.append(new_row)
        self.array = new_array
        self.cols = 2*self.cols



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