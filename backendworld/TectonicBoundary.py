from backendworld.WorldAttribute import WorldAttribute
from Position import Position
from backendstorage.Vertices.Vertex import Vertex

class TectonicBoundary(WorldAttribute):
    # TODO:
    #  PRIORITY 1
    #  Needs logic to maintain self._dataStorageVertices depending on Cells / TectonicCells
    """
        A boundary dividing TectonicPlates within a world
    """
    def __init__(self, **kwargs):
        self.originVertex = None
        self.destinationVertex = None
        self.tectonicCells = set()
        self._dataStorageVertices = set()
        super(TectonicBoundary, self).__init__(**kwargs)

    def set_end(self, pt: Position, orig: bool = False, dest: bool = False):
        """
        Ability to set one or both ends of the boundary to a given Position
        :param pt: The Position to set to
        :param orig: Boolean - setting origin
        :param dest: Boolean - setting destination
        :return:
        """
        # TODO:
        #  PRIORITY 1
        #  Needs logic to apply this change to the rest of the data storage
        #  Use with caution right now
        if orig == True:
            self.originVertex = pt
        if dest == True:
            self.destinationVertex = pt