from PIL import ImageFont
import importlib
import os
import logging
import time
import math

# TODO: THIS FILE NEEDS DOCSTRINGS
#doing
class Conf:
    """
    A bunch of shared configuration stuff goes here.
    A lot of the user's commands through UI will probably be changing these
    """
    classes = {
        'GridCell':'backendstorage.Cells.GridCell',
        'Cell': 'backendstorage.Cells.Cell',
        'VertexPoint': 'backendstorage.Vertices.VertexPoint',
        'GridStructure': 'backendstorage.StorageMechanisms.GridStructure',
        'TectonicCell': 'backendworld.TectonicCell',
        'ShapelyStructure': 'backendstorage.StorageMechanisms.ShapelyStructure'

    }
    def __init__(self):
        self.world = None
        self.startTimeInt = self.time_id()
        self.logFolder = 'logs/'
        self.logsSaved = 1
        self.logfilename = self.logFolder + '{}_backendlog.log'.format(self.startTimeInt)
        self.config_log()
        self.clear_logs()

        self.resourceFolder = 'resources/'
        self.fontLocation = self.resourceFolder + '07558_CenturyGothic.ttf'
        self.fontExtensions = ['.ttf']


        # self.cellClass = 'TectonicCell'
        # self.cellModule = 'backendworld.TectonicCell'

        self.flatImageFolder = 'flatImages/'
        self.gifName = self.flatImageFolder + 'out.gif'
        self.imageName = self.flatImageFolder + '{}/image_{}'
        self.defaultImageExtension = 'jpg'
        self.imageHeight = 1200
        self.imageWidth = int(1.5*self.imageHeight)
        self.gifFrameDuration = 1000

        self.ageGradient = ((130, 245, 0), (244,0,245))

        # self.ShapelyStructureColumns = ['ShapelyCell', 'TectonicCell','geometry','pos']
        self.ShapelyStructureColumns = [
            'ShapelyCell', 'TectonicCell', 'geometry', 'pos', 'age_diff','pos_point','stack_size','speed'
        ]

        self.fnt = self.set_font(self.fontLocation, size=100)
        self.fnt_sm = self.set_font(self.fontLocation, size=20)
        self.imageGrayscale = 0.8
        self.imageCaption = "Age: {}"
        self.imageSmallCaptionPos = (20,20)
        self.imageAnnotationProperties = {'anchor':'lt', 'fill':(
            int(255 * self.imageGrayscale), int(255 * self.imageGrayscale), int(255 * self.imageGrayscale), int(255 * self.imageGrayscale)), 'stroke_width':1,
                             'font':self.fnt_sm}


        self.make_necessary_folders()



    # ------------------------------------
    # Functions needed for conf to work
    # ------------------------------------

    # If you know the name of the class and the module/package of the class, can use str to specify class name
    # Thanks stackoverflow https://stackoverflow.com/questions/1176136/convert-string-to-python-class-object
    def class_for_name(self, class_name, module_name=None):
        """
        :param class_name: the class we're loading
        :param module_name: the module we're loading
        :return: loads module and class, raises errors if wrongs
        """
        try:
            if module_name is None and class_name in Conf.classes:
                module_name = Conf.classes[class_name]
            # load the module, will raise ImportError if module cannot be loaded
            m = importlib.import_module(module_name)
            # get the class, will raise AttributeError if class cannot be found
            c = getattr(m, class_name)
            return c
        except ImportError as e:
            print("{} wrong module {}".format(e, module_name))
            self.log_from_conf('error', "Module {} could not be found".format(module_name))
        except AttributeError as e:
            print("{} wrong class {} in module {}".format(e, class_name, module_name))
            self.log_from_conf('error', "Class {} could not be found in module".format(class_name, module_name))
        return


    def time_id(self):
        '''

        :return: start time modded with the starttimeoffset
        '''
        startTime = time.time()
        startTimeOffset = pow(10, math.ceil(math.log(7 * 24 * 60 * 60, 10)))
        return int(startTime) % (startTimeOffset)

    def clear_logs(self):
        '''

        :return: removes logs starting with the oldest and removes logs that over a week old.
        '''
        existing_logs = os.listdir(self.logFolder)
        if len(existing_logs) == 0:
            return
        new_log = os.path.basename(self.logfilename)
        while max(existing_logs).split('_')[0]>str(new_log).split('_')[0]:
            self.log_from_conf('info', 'Removing log {} that is more than a week old'.format(max(existing_logs)))
            os.remove(self.logFolder+max(existing_logs))
            existing_logs.remove(max(existing_logs))
        while (self.logsSaved < len(existing_logs)):
            oldest = min(existing_logs)
            self.log_from_conf('info', 'Removing oldest log {}'.format(min(existing_logs)))
            os.remove(self.logFolder + min(existing_logs))
            existing_logs.remove(oldest)

    def make_necessary_folders(self, given_folders=None):
        '''

        :param given_folders: folder that it is given to check
        :return: if the folders needed aren't here makes them.
        '''
        if type(given_folders) is str:
            given_folders = [given_folders]
        elif given_folders is None:
            known_folders = [self.flatImageFolder, self.resourceFolder, self.logFolder]
            given_folders = known_folders

        for folder in given_folders:
            try:
                os.mkdir(os.path.dirname(folder))
                logging.info("New directory {} had to be created".format(str(os.path.dirname(folder))))

            except OSError as error:
                pass

    def config_log(self, level=logging.DEBUG, filename=None):
        '''

        :param level: the level the config log thing is at
        :param filename: filename checking to see if it is there
        :return: if the log isn't there makes it
        '''
        if filename is None:
            filename = self.logfilename
        if '.log' not in filename:
            filename += '.log'
        self.make_necessary_folders(given_folders=filename)
        logging.basicConfig(filename=filename,
                            level=level,
                            format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')

    def log_from_conf(self, level, message):
        '''

        :param level: different levels of things that could be logged.
        :param message: the message that goes with the thing logged that has happeend.
        :return: checks log and shows what status and message of it are
        '''
        levels = {'critical': logging.critical, 'error':logging.error, 'warning':logging.warning, 'info':logging.info, 'debug':logging.debug}
        if level in levels:
            levels[level](message)

    def set_font(self, fontfile, size):
        '''

        :param fontfile: file font is stored in
        :param size: size of the file
        :return: sets font does error checking if it isn't found, sets the fontfile& size.
        '''
        try:
            fnt = ImageFont.truetype(fontfile, size)
        except OSError:
            self.log_from_conf('info', "Specified font {} could not be found on system".format(self.fontLocation))
            fontfile = self._fix_fonts()
            fnt = self.set_font(fontfile,size)

        return fnt



    def _search_for_fonts(self, given_location=None, font_extensions=None, ignore_dot_files=True):
        '''

        :param given_location: the location given that we looking in for the font
        :param font_extensions: if there are any font extensions (there are none right now)
        :param ignore_dot_files: files to be ignored (right now set to none)
        :return: searches for fonts, returns errors if no fonts are found.
        '''
        fonts = {}
        if font_extensions is None:
            font_extensions = self.fontExtensions

        if given_location is None:
            given_location = os.getcwd()

        for root, dirs, files in os.walk(given_location, topdown=True):
            if ignore_dot_files is True:
                files = [f for f in files if not f[0] == '.']
                dirs[:] = [d for d in dirs if not d[0] == '.']
            for name in files:
                if '.' in name:
                    ext = name.rsplit('.')[-1]
                    if ext in font_extensions or '.' + ext in font_extensions:
                        fonts[name] = {'path': os.path.join(root, name), 'extension': ext, 'filename': name}
        if len(fonts) == 0:
            self.log_from_conf('warning', 'No fonts installed')
        return fonts

    def _fix_fonts(self):
        '''

        :return:shows the fonts that have been found & where
        '''
        fonts = self._search_for_fonts()

        self.log_from_conf('info', 'Found {} fonts'.format(len(fonts)))

        return fonts[list(fonts)[0]]['path']


