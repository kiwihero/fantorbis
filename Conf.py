from PIL import ImageFont
import importlib

class Conf:
    def __init__(self):
        self.fontLocation = '07558_CenturyGothic.ttf'
        self.structureClass = 'GridStructure'
        self.structureModule = 'backendstorage.GridStructure'

        self.gifName = 'out.gif'
        self.imageName = 'image_{}'
        self.defaultImageExtension = 'jpg'

        self.fnt = ImageFont.truetype(self.fontLocation, 100)
        self.fnt_sm = ImageFont.truetype(self.fontLocation, 20)
        self.imageGrayscale = 0.8
        self.imageCaption = "Age: {}"
        self.imageSmallCaptionPos = (20,20)
        # self.imageAnnotationProperties = {"anchor": "lt","stroke_width":1}
        self.imageAnnotationProperties = {'anchor':'lt', 'fill':(
            int(255 * self.imageGrayscale), int(255 * self.imageGrayscale), int(255 * self.imageGrayscale), int(255 * self.imageGrayscale)), 'stroke_width':1,
                             'font':self.fnt_sm}

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