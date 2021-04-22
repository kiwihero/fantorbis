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

class MessageError(_GenericError):
    def __init__(self, message):
        self.message = message