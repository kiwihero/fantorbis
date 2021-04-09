from backendworld.WorldAttribute import WorldAttribute

class TectonicBoundary(WorldAttribute):
    """
        A boundary dividing TectonicPlates within a world
    """
    def __init__(self, **kwargs):

        self.originVertex = None
        self.destinationVertex = None
        self.tectonicCells = set()
        self._dataStorageVertices = set()
        super(TectonicBoundary, self).__init__(**kwargs)
