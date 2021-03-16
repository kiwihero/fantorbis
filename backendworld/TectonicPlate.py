from backendworld.WorldAttribute import WorldAttribute

class TectonicPlate(WorldAttribute):
    def __init__(self, **kwargs):
        self.cells = set()
        super(TectonicPlate, self).__init__(**kwargs)