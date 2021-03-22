import importlib

class Conf:
    def __init__(self):
        self.fontLocation = '/Users/mancia2/PycharmProjects/SoftwareEngMaps/fantorbis/07558_CenturyGothic.ttf'
        self.structureClass = 'GridStructure'
        self.structureModule = 'backendstorage.GridStructure'

    def class_for_name(self, module_name, class_name):
        # load the module, will raise ImportError if module cannot be loaded
        m = importlib.import_module(module_name)
        # get the class, will raise AttributeError if class cannot be found
        c = getattr(m, class_name)
        return c