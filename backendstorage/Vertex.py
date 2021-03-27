class Vertex:
    def __init__(self, customkwargs=None, **kwargs):
        self.originVertex = None
        self.destinationVertex = None
        self.vertices = set()

    def addVertex(self, vertex):
        return Exception

    def removeVertex(self, vertex):
        return Exception

    def splitVertex(self, vertexPoint1, vertexPoint2):
        return Exception

    def insertVertex(self, vertexPoint1, vertexPoint2, newVertexPoint):
        return Exception
