import copy
from Position import Position
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
        r = 0
        while self.rows > len(self.array):
            row = []
            for c in range(self.cols):
                if self.createElem != None:
                    print("creating elem {}, with kwargs {}".format(self.createElem, self.createElemKwargs))

                    if self.createElemKwargs is None:
                        elem = self.createElem(**kwargs)
                    else:
                        if 'include_TwoDimensionalArray_pos' in self.createElemKwargs:
                            p = Position(c,r)
                            print("INCLUDING POSITION", p)
                            self.createElemKwargs['TwoDimensionalArray_pos'] = p
                        elem = self.createElem(**self.createElemKwargs, **kwargs)
                    print("created the elem {}".format(elem))
                    row.append(elem)
                else:
                    row.append(self.defaultElem)
            self.array.append(row)
            r += 1

    def __iter__(self):
        """
        Allows for iteration
        Iterates from 0th row to last row, and within each row from 0th to last column
        E.G. for an array of r rows and c columns,
        [0][0], [0][1], ..., [0][c],
        [1][0], [1][1], ..., [1][c],
        ...,
        [r][0], [r][1], ..., [r][c]
        :return:
        """
        return _TwoDimensionalArrayIterator(self.array)

    def __getitem__(self, item):
        """
        Allows retrieval of items using instance[i][j]
        :param item: i
        :return:
        """
        return self.array[item]

    def __setitem__(self, key: int, value):
        """
        Ability to set an entire row of the array
        :param key: integer of which row to be set, 0 <= value <= self.rows
        :param value: A new row, of the same length as existing rows: len(key) == self.cols
        :return:
        """
        # TODO: Add error checking to make sure 'value' argument is some sort of list
        #  (e.g. 'aaa' is not a valid input when self.cols==3 despite len('aaa') == 3)
        if key < 0 or key >= self.rows:
            raise IndexError("Row index {} out of bounds, must be between 0 and {}".format(key, self.rows-1))
        if len(value) != self.cols:
            raise ValueError("New row {} must be of length {}".format(value, self.cols))
        self.array[key] = value

    def print_contents(self):
        """
        Iterate through, printing all elements as grid
        :return:
        """
        print(self.return_contents())


    def return_contents(self):
        """
        Helper function for print_contents
        Or use on its own if you want the string instead of printed
        :return:
        """
        outstr = ''
        if type(self.array) is list:
            outstr += "Printing contents of {} x {} array\n".format(self.rows, self.cols)
            for row in self.array:
                # print("row of len", len(row))
                printed_row = ''
                for col in row:
                    printed_row += str(col) + ' '
                outstr += printed_row + "\n"
            return outstr
        else:
            return "Oops! Array {} not correct type {}".format(self.array, type(self.array))


    def grid_print(self):
        """
        The fancy ascii version of print_contents
        :return:
        """
        if type(self.array) is list:
            rowstr_len = len(str(self.rows))
            colstr_len = max(len(str(self.cols)),5)
            print("Printing grid of {} x {} array".format(self.rows, self.cols))
            header_str = ' '*rowstr_len + '||'
            div_str = '-'*rowstr_len + '++'
            for c in range(self.cols):
                sub_header = str(c)
                while (len(sub_header) < colstr_len):
                    if (len(sub_header)+2) < colstr_len:
                        sub_header += ' '
                    sub_header = ' ' + sub_header
                header_str += sub_header
                div_str += '-' * len(sub_header)
                header_str += '|'
                div_str += '+'
            print(header_str)
            print(div_str)
            r = 0
            for row in self.array:
                # print("row of len", len(row))
                printed_row = '{}|'.format(r)
                while(len(printed_row) <= rowstr_len):
                    printed_row = ' ' + printed_row
                printed_row += '|'
                for col in row:
                    printed_row += '{0:>5}|'.format(str(col))
                # printed_row += '|'
                print(printed_row)
                r += 1
            print(div_str)
        else:
            print("Oops! Array {} not correct type {}".format(self.array, type(self.array)))

    def __str__(self):
        """
        Single-line string description
        :return:
        """
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
        """
        Returns the index of the first element with the specified value
        Raises ValueError if cell cannot be found
        Can specify parts of array. For example, rowstart=1 rowend=3 colstart = 2 colend = 4 on a 5x5:
        ||   0 |   1 |   2 |   3 |   4 |
        -++-----+-----+-----+-----+-----+
        0||     |     |     |     |     |
        1||     |     |    x|    x|     |
        2||     |     |    x|    x|     |
        3||     |     |     |     |     |
        4||     |     |     |     |     |
        -++-----+-----+-----+-----+-----+
        Looks at elements where row index >=1, row index <3, column index >= 2, column index < 4
        :param cell: Element sought
        :param rowstart: Start of each row to search
        :param rowend: End of each row to search
        :param colstart: Start of each col to search
        :param colend: End of each col to search
        :return: List of length two, format [row,col] of first index of cell
        """
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
        raise ValueError()

    def clear(self):
        """Remove all elements, leaving 0x0 array"""
        self.array = []
        self.rows = 0
        self.cols = 0

    def insert(self, index: int, row: list):
        """
        Insert a new row to the array, extending the number of rows rather than replacing the existing index
        Use __setitem__ to replace rather than extending
        :param index: integer of which row to be set, 0 <= value <= self.rows
        :param row: A new row, of the same length as existing rows: len(key) == self.cols
        :return:
        """
        # TODO: Add checks for invalid inputs to index, row
        if len(row) == self.cols:
            self.array.insert(index, row)
            self.rows += 1
        else:
            raise ValueError()

    def append(self, row:list):
        """
        Similar to insert but at end of list
        :param row: A new row, of the same length as existing rows: len(key) == self.cols
        :return:
        """
        # TODO: Add checks for invalid inputs to row
        if len(row) == self.cols:
            self.array.append(row)
            self.rows+= 1
        else:
            raise ValueError()

    def count(self, cell, rowstart=0, rowend=None, colstart=0, colend=None):
        """
        Count all instances of cell
        Arguments as in index(self, cell, rowstart=0, rowend=None, colstart=0, colend=None)
        :param cell:
        :param rowstart:
        :param rowend:
        :param colstart:
        :param colend:
        :return: Number of occurrences, 0 being a valid return if cell cannot be found
        """
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

    def __contains__(self, key):
        """
        Allows for the use of the 'in' keyword
        :param key: Element to be tested for
        :return: boolean
        """
        if self.count(key) == 0:
            return False
        return True

    def find_attrs(self,attrDict,rowstart=0, rowend=None, colstart=0, colend=None):
        """
        Ability to search for elements that are themselves classes with attributes and attribute values given in attrDict
        Start and end functionality as in index(self, cell, rowstart=0, rowend=None, colstart=0, colend=None)
        :param attrDict: A dictionary of attributes and their values an element of the array must contain to be counted
        :param rowstart:
        :param rowend:
        :param colstart:
        :param colend:
        :return: List of length two, format [row,col] of first index of cell with all attributes of attrDict
        """
        if rowend is None:
            rowend = self.rows
        if colend is None:
            colend = self.cols
        for row in range(rowstart, rowend):
            for col in range(colstart, colend):
                cell = self[row][col]
                match = True
                for attr, val in attrDict.items():
                    if cell.attr != val:
                        match=False
                        break #If one attribute doesn't work, stop comparing attributes: gets back to for loop going through the array
                if match == True:
                    return [col, row]
        raise ValueError()

    def find_id(self,address=None,cell=None):
        """
        Iteration through the array's elements to find one with the given object id
        :param address: ID requested
        :param cell: Can also look by the id of a given object
        :return: List of length two, format [row,col] of first index of cell with all attributes of attrDict
        """
        if address == None:
            if cell != None:
                address = hex(id(cell))
            else:
                return Exception
        for row in range(self.rows):
            for col in range(self.cols):
                if hex(id(self[row][col])) == address:
                    return [col,row]

    def subdivide(self):
        """
        Subdivides each cell horizontally and vertically
        :return:
        """
        # TODO: Add argument, functionality for possibility of deep copying of elements
        self.grid_print()
        print("subdivision not yet started")
        self.subdivide_rows()
        self.subdivide_cols()
        print("subdivision done")
        self.grid_print()

    def subdivide_rows(self):
        """
        Within each row, the cell becomes two cells
        Array now has twice as many cols and same number of rows
        Elements are shallowly copied
        :return:
        """
        # TODO: Add argument, functionality for possibility of deep copying of elements
        new_array = []
        for row in range(self.rows):
            new_row = []
            for col in range(self.cols):
                old_cell = self.array[row][col]
                print("\n\n\nrow {} column {}".format(row,col))
                print("CELL TYPE {}, cell {}".format(type(old_cell),old_cell))
                try:
                    new_cell = old_cell.copy(copy_method='subdivision')
                except TypeError as e:
                    new_cell = copy.copy(old_cell)
                if 'include_TwoDimensionalArray_pos' in self.createElemKwargs:
                    old_pos = Position(col, len(new_array))
                    old_cell.dataStoragePosition = old_pos
                    new_pos = Position(col, len(new_array) + 1)
                    new_cell.dataStoragePosition = new_pos
                    print("subdivision old position {}, new position {}".format(old_cell.dataStoragePosition, new_cell.dataStoragePosition))
                new_row.append(new_cell)
                self.array[row][col] = old_cell
            print("ROWS TO ADD")
            out1 = ''
            for elem in self.array[row]:
                out1+= str(elem) + " "
            out2 = ''
            for elem in new_row:
                out2 += str(elem) + " "
            print(out1)
            print(out2)
            print("END ROWS TO ADD")
            new_array.append(self.array[row])
            new_array.append(new_row)
        self.array = new_array
        self.rows = len(self.array)



    def subdivide_cols(self):
        """
        Within each column, the cell becomes two cells
        Array now has twice as many rows and same number of cols
        Elements are shallowly copied
        :return:
        """
        # TODO: Add argument, functionality for possibility of deep copying of elements
        new_array = []
        for row in range(self.rows):
            new_row = []
            for col in range(self.cols):
                # print("col {} new row (len {}): {}".format(col, len(new_row), new_row))
                old_cell = self.array[row][col]
                try:
                    new_cell = old_cell.copy(copy_method='subdivision')
                except TypeError as e:
                    new_cell = copy.copy(old_cell)
                # new_cell = copy.copy(old_cell)
                if 'include_TwoDimensionalArray_pos' in self.createElemKwargs:
                    old_pos = Position(len(new_row), row)
                    old_cell.dataStoragePosition = old_pos
                    new_pos = Position(len(new_row)+1, row)
                    new_cell.dataStoragePosition = new_pos
                    # print("column subdivision old position {}, new position {}".format(old_cell.ds_pos, new_cell.ds_pos))
                new_row.append(old_cell)
                new_row.append(new_cell)
            new_array.append(new_row)

        self.array = new_array
        self.cols = len(self.array[0])


class _TwoDimensionalArrayIterator:
    """
    Iterator helper class
    """
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

# Uncomment and run  class to see some examples of class methods in use

# t1 = TwoDimensionalArray(rows=2, cols=2)
# t1[0]=[6,5]
# t1[1]=[4,3]
# t1[0][0]=9
# t1.grid_print()
# t1.subdivide()
# t1.grid_print()
# t1.print_contents()