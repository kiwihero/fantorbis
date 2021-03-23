class GeneralStructure:
    def __init__(self, **kwargs):
        self._ArrayStorage = None
        self.cellShape = None

    def print_contents(self):
        raise DoesNotExistError("ArrayStorage")


    def __iter__(self):
        raise DoesNotExistError("ArrayStorage")


    def __str__(self):
        return 'Data structure of some sort'.format()

    def swap_cells(self, cell1, cell2):
        tmp = cell1.pos
        self.move_cell(cell1,cell2.pos)
        self.move_cell(cell2, tmp)

    def move_cell(self, cell, destination):
        raise StructureNotImplementedError("move_cell")

    def add_cell(self, cell):
        raise StructureNotImplementedError("move_cell")

    def remove_cell(self, cell):
        raise StructureNotImplementedError("move_cell")

class _GenericError(Exception):
    pass

class StructureNotImplementedError(_GenericError):
    def __init__(self, methodname):
        self.message = "The method {} has not been defined for this class!".format(methodname)

class DoesNotExistError(_GenericError):
    def __init__(self, variablename):
        self.message = "The variable {} has not been defined for this class!".format(variablename)

class WrongTypeError(_GenericError):
    def __init__(self, variablename, actualtype, requiredtype):
        self.message = "The variable {} of type {} is required to be {} type!".format(variablename, actualtype, requiredtype)

class GeneralIterator:
    def __next__(self):
        raise StructureNotImplementedError("Iteration")