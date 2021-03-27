# All of the structures inherit this
# Declares some methods expected, default to returning an error when those are called and not implemented in inherited
class GeneralStructure:
    def __init__(self, conf=None, **kwargs):
        self._ArrayStorage = None
        self.cellShape = None
        self.conf = conf
        self.cellClassName = 'GridCell'
        self.cellClassFile = 'backendstorage.GridCell'
        if self.conf is not None:
            self.cellClass = self.conf.class_for_name(module_name=self.cellClassFile, class_name=self.cellClassName)
        else:
            raise DoesNotExistError("self.conf")

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

    def move_cell(self, cell, **kwargs):
        raise StructureNotImplementedError("move_cell")

    def add_cell(self, cell):
        raise StructureNotImplementedError("move_cell")

    def remove_cell(self, cell):
        raise StructureNotImplementedError("move_cell")

    def subdivide(self):
        raise StructureNotImplementedError("subdivide")

    def subdivide_rows(self):
        raise StructureNotImplementedError("subdivide_rows")

    def subdivide_cols(self):
        raise StructureNotImplementedError("subdivide_cols")

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

