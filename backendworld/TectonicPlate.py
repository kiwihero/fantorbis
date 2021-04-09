from backendworld.WorldAttribute import WorldAttribute

class TectonicPlate(WorldAttribute):
    """
    A collection of TectonicCell objects making up one plate of a World
    """
    def __init__(self, **kwargs):
        self._cells = set()
        super(TectonicPlate, self).__init__(**kwargs)