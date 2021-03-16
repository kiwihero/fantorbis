class GeneralStructure:
    def __init__(self, **kwargs):
        self.ArrayStorage = None

    def print_contents(self):
        raise DoesNotExistError("ArrayStorage")


    def __iter__(self):
        raise DoesNotExistError("ArrayStorage")


    def __str__(self):
        return 'Data structure of some sort'.format()

    def move_cell(self, cell, destination):
        raise StructureNotImplementedError("move_cell")

    def add_cell(self, cell):
        raise StructureNotImplementedError("move_cell")

    def remove_cell(self, cell):
        raise StructureNotImplementedError("move_cell")

class GenericError(Exception):
    pass

class StructureNotImplementedError(GenericError):
    def __init__(self, methodname):
        self.message = "The method {} has not been defined for this class!".format(methodname)

class DoesNotExistError(GenericError):
    def __init__(self, variablename):
        self.message = "The variable {} has not been defined for this class!".format(variablename)

class WrongTypeError(GenericError):
    def __init__(self, variablename, actualtype, requiredtype):
        self.message = "The variable {} of type {} is required to be {} type!".format(variablename, actualtype, requiredtype)

class GeneralIterator:
    def __next__(self):
        raise StructureNotImplementedError("Iteration")