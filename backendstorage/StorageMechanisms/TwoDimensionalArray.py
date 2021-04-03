import copy
class TwoDimensionalArray(list):
    """
    List of lists, has some helpful functions
    """

    def __init__(self, rows=0, cols=0, defaultElem=None, createElem=None, createElemKwargs=None, **kwargs):
        super(TwoDimensionalArray, self).__init__(**kwargs)
        self.array = []
        self.rows = rows
        self.cols = cols
        self.defaultElem = defaultElem
        self.createElem = createElem
        print("elem kwargs {}".format(createElemKwargs))
        if createElemKwargs is not None:
            self.createElemKwargs = createElemKwargs
        else:
            self.createElemKwargs = {}
        self.createElemKwargs['parent'] = self
        while (self.rows > len(self.array)):
            row = []
            for c in range(self.cols):
                if self.createElem != None:
                    print("creating elem {}, with kwargs {}".format(self.createElem, self.createElemKwargs))

                    if self.createElemKwargs is None:
                        elem = self.createElem(**kwargs)
                    else:
                        elem = self.createElem(**self.createElemKwargs, **kwargs)
                    print("created the elem {}".format(elem))
                    row.append(elem)
                else:
                    row.append(self.defaultElem)
            self.array.append(row)

    def __iter__(self):
        return _TwoDimensionalArrayIterator(self.array)

    def __getitem__(self, item):
        """
        Allows retrieval of items using instance[i][j]
        :param item:
        :return:
        """
        return self.array[item]

    def __setitem__(self, key, value):
        print("setting key {}, value {}".format(key,value))
        self.array[key] = value

    def print_contents(self):
        if type(self.array) is list:
            print("Printing contents of {} x {} array".format(self.rows, self.cols))
            for row in self.array:
                # print("row of len", len(row))
                printed_row = ''
                for col in row:
                    printed_row += str(col) + ' '
                print(printed_row)
        else:
            print("Oops! Array {} not correct type {}".format(self.array, type(self.array)))

    def grid_print(self):
        max = 0
        if type(self.array) is list:
            print("Printing grid of {} x {} array".format(self.rows, self.cols))
            for row in self.array:
                # print("row of len", len(row))
                printed_row = '|'
                for col in row:
                    printed_row += '{0:>5}|'.format(str(col))
                # printed_row += '|'
                print(printed_row)
        else:
            print("Oops! Array {} not correct type {}".format(self.array, type(self.array)))

    def __str__(self):
        outstr = ""
        if type(self.array) is list:
            outstr += '{} by {} 2d list '.format(self.rows, self.cols)
            outstr += '['
            for row in self.array:
                # print("row of len", len(row))
                printed_row = '['
                for col in row:
                    printed_row += str(col) + ' '
                printed_row += ']'
                outstr += printed_row
            outstr += ']'
            return outstr
        else:
            return super(TwoDimensionalArray, self).__str__()

    def index(self, cell, rowstart=0, rowend=None, colstart=0, colend=None):
        if rowstart > self.rows:
            rowstart = self.rows
        if rowend is None or rowend > self.rows or rowend < rowstart:
            rowend = self.rows
        if colstart > self.cols:
            colstart = self.cols
        if colend is None or colend > self.cols or colend < colstart:
            colend = self.cols
        for row in range(rowstart, rowend):
            for col in range(colstart, colend):
                if self[row][col] == cell:
                    return [col, row]
        return ValueError

    def clear(self):
        self.array = []
        self.rows = 0
        self.cols = 0

    def insert(self, index: int, row: list):
        if len(row) == self.cols:
            self.array.insert(index, row)
            self.rows += 1
        else:
            raise ValueError

    def append(self, row:list):
        if len(row) == self.cols:
            self.array.append(row)
            self.rows+= 1
        else:
            raise ValueError

    def count(self, cell, rowstart=0, rowend=None, colstart=0, colend=None):
        count = 0
        if rowstart > self.rows:
            rowstart = self.rows
        if rowend is None or rowend > self.rows or rowend < rowstart:
            rowend = self.rows
        if colstart > self.cols:
            colstart = self.cols
        if colend is None or colend > self.cols or colend < colstart:
            colend = self.cols
        for row in range(rowstart, rowend):
            for col in range(colstart, colend):
                if self[row][col] == cell:
                    count += 1
        return count

    def find_attrs(self,attrDict,rowstart=0, rowend=None, colstart=0, colend=None):
        if rowend is None:
            rowend = self.rows
        if colend is None:
            colend = self.cols
        for row in range(rowstart, rowend):
            for col in range(colstart, colend):
                cell = self[row][col]
                match=True
                for attr, val in attrDict.items():
                    if cell.attr != val:
                        match=False
                        break #If one attribute doesn't work, stop comparing attributes: gets back to for loop going through the array
                if match == True:
                    return [col, row]
        raise ValueError

    def find_address(self,address=None,cell=None):
        if address == None:
            if cell != None:
                address = hex(id(cell))
            else:
                return Exception
        for row in range(self.rows):
            for col in range(self.cols):
                if hex(id(self[row][col])) == address:
                    return [col,row]
#
#     def swap_pos(self, originRow, originCol, destRow, destCol):
#         temp_cell = self.remove_pos(originRow,originCol)
#         self.move_pos(destRow,destCol,originRow,originCol)
#         self.add_pos(temp_cell, destRow, destCol)
#
#
#     def move_pos(self, originRow, originCol, destRow, destCol):
#         cell = self.lookupPosition(row=originRow,col=originCol)
#         print("moving cell in array {}".format(cell))
#         self.add_pos(cell, destRow, destCol)
#         if self.createElem != None:
#             elem = self.createElem(customkwargs=self.elemKwargs)
#             self.add_pos(elem, originRow, originCol)
#
#         else:
#             self.add_pos(self.defaultElem, originRow, originCol)
#         print("cell now at ".format(self.search_for_cell(cell)))
#
#
#     def add_pos(self, cell, row, col):
#         print("adding to pos {},{}".format(row, col))
#         row = row % len(self.array)
#         col = col % len(self.array[row])
#         print("adding to moded pos {},{}".format(row,col))
#         self.array[row][col] = cell
#         print("array row {} col {} now {}".format(row,col,self.array[row][col]))
#
#     def remove_pos(self, row, col):
#         cell = self.lookupPosition(row,col)
#         if self.createElem != None:
#             self.array[row][col] = self.createElem()
#         else:
#             self.array[row][col] = self.defaultElem
#         return cell
#
    def subdivide(self):
        self.subdivide_rows()
        self.subdivide_cols()
        # print("size now rows {}, cols {}".format(self.rows,self.cols))

    def subdivide_rows(self):
        new_array = []
        for row in range(self.rows):
            new_row = []
            for col in range(self.cols):
                old_cell = self.array[row][col]
                # print("CELL TYPE {}, cell {}".format(type(old_cell),old_cell))
                new_cell = copy.copy(old_cell)
                # new_cell = old_cell.copy()
                new_row.append(new_cell)
            new_array.append(self.array[row])
            new_array.append(new_row)
        self.array = new_array
        self.rows = len(self.array)



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
        self.cols = len(self.array[0])

#
#
#
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
t1 = TwoDimensionalArray(rows=2, cols=2)
t1[0]=[6,5]
t1[1]=[4,3]
t1[0][0]=9
t1.grid_print()
t1.subdivide()
t1.grid_print()