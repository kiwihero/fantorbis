from pyproj._crs import _CRS

class _FantasyCRS(_CRS):
    def __init__(self, **kwargs):
        super(_FantasyCRS, self).__init__(**kwargs)