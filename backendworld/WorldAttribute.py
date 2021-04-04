class WorldAttribute:
    def __init__(self, world=None):
        self.world = world

    def setWorld(self, world):
        self.world = world

    def __copy__(self):
        new_attr = WorldAttribute()
        self.copy_attrs(new_attr)
        return new_attr

    def copy_attrs(self, dest):
        """
        Copies all attributes of self onto another instance
        :return:
        """
        attrs = {}
        attrs['world'] = self.world
        for key, value in attrs.items():
            dest.key = value
        return attrs

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