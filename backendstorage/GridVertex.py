from backendstorage.Vertex import Vertex
class GridVertex(Vertex):
    def __init__(self):
        super(Vertex, self).__init__(**kwargs)
        self.parent = parent
        self.ckwargs = customkwargs
        self.kwargs = kwargs
        if self.ckwargs is None:
            self.ckwargs = {}