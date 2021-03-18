from backendworld.WorldAttribute import WorldAttribute

class TectonicCell(WorldAttribute):
    def __init__(self, **kwargs):
        self.age = 0
        super(TectonicCell, self).__init__(**kwargs)