from backendworld.WorldAttribute import WorldAttribute

class TectonicBoundary(WorldAttribute):
    def __init__(self, **kwargs):
        self.origin = None
        self.destination = None
        super(TectonicBoundary, self).__init__(**kwargs)