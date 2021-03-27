import backendstorage.CustomExceptions
class Vertex:
    def __init__(self):
        self.originVertexPoint = None
        self.destinationVertexPoint = None
        self.vertexSegments = set()
        self.orderedVertexSegments = []

    def add_vertex_segment(self, vertex_segment):
        '''
        Extend an existing vertex using a vertex segment that connects
        :param vertex_segment: A single vertex segment that is contiguous with existing vertex
        :return: none
        '''
        if len({self.originVertexPoint,self.destinationVertexPoint} & vertex_segment.points()) == 0:
            for existing_segment in self.vertexSegments:
                if existing_segment.is_contiguous(vertex_segment):
                    # TODO: Make multi-vertices when adding a segment in the middle of a vertex
                    return
            return backendstorage.CustomExceptions.MessageError(
                "The segment {} is not contiguous with the vertex {}".format(vertex_segment, self))
        elif self.originVertexPoint in vertex_segment.points():


        self.vertexSegments.add(vertex_segment)
#         return Exception
#
#     def removeVertex(self, vertex):
#         return Exception
#
#     def splitVertex(self, vertexPoint1, vertexPoint2):
#         return Exception
#
#     def insertVertex(self, vertexPoint1, vertexPoint2, newVertexPoint):
#         return Exception
