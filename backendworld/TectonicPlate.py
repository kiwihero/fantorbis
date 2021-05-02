from shapely.ops import unary_union

from backendworld.WorldAttribute import WorldAttribute

class TectonicPlate(WorldAttribute):
    """
    A collection of TectonicCell objects making up one plate of a World
    """
    def __init__(self, **kwargs):
        self._cells = set()
        self._plate_boundary = None
        super(TectonicPlate, self).__init__(**kwargs)

    def update_boundary(self):
        plate_face =unary_union(self._cells)
        boundary = plate_face.boundary
        self._plate_boundary = boundary
        return self._plate_boundary
