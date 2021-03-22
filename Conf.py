import importlib

class Conf:
    def __init__(self):
        # You can put whatever here it doesn't have to be century gothic
        self.fontLocation = '/Users/mancia2/PycharmProjects/SoftwareEngMaps/fantorbis/07558_CenturyGothic.ttf'

        # Change this to change how the data is stored
        self.structureClass = 'GridStructure'
        self.structureModule = 'backendstorage.GridStructure'

        self.gifName = 'out.gif'

    # ------------------------------------
    # Functions needed for conf to work
    # ------------------------------------

    # If you know the name of the class and the module/package of the class
    # Thanks stackoverflow https://stackoverflow.com/questions/1176136/convert-string-to-python-class-object
    def class_for_name(self, module_name, class_name):
        # load the module, will raise ImportError if module cannot be loaded
        m = importlib.import_module(module_name)
        # get the class, will raise AttributeError if class cannot be found
        c = getattr(m, class_name)
        return c