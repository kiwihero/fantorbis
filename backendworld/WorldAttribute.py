class WorldAttribute:
    def __init__(self, world=None):
        self.world = world

    def setWorld(self, world):
        self.world = world

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
            self.message = "The variable {} of type {} is required to be {} type!".format(variablename, actualtype,
                                                                                          requiredtype)