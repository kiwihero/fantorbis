import backendstorage.CustomExceptions
class Vertex:
    def __init__(self):
        self.originVertexPoint = None
        self.destinationVertexPoint = None
        self.vertexSegments = set()
        self.orderedVertexSegments = []

    def add_vertex_segment(self, vertex_segment):
        """
        Extend an existing vertex using a vertex segment that connects
        :param vertex_segment: A single vertex segment that is contiguous with existing vertex
        :return: error if applicable
        """
        shared_points = {self.originVertexPoint,self.destinationVertexPoint} & vertex_segment.points()
        if len(shared_points) == 0:
            for existing_segment in self.vertexSegments:
                if existing_segment.is_contiguous(vertex_segment):
                    self.vertexSegments.add(vertex_segment)
                    # TODO: Make multi-vertices when adding a segment in the middle of a vertex
                    return
            return backendstorage.CustomExceptions.MessageError(
                "The segment {} is not contiguous with the vertex {}".format(vertex_segment, self))
        else:
            new_point = vertex_segment.points() - shared_points
            if len(new_point) == 0:
                return backendstorage.CustomExceptions.MessageError(
                    "The segment {} does not add to the vertex {}".format(vertex_segment, self))
            elif self.originVertexPoint in shared_points:
                self.originVertexPoint = new_point
            else:
                self.destinationVertexPoint = new_point
            self.vertexSegments.add(vertex_segment)

    # def remove_vertex_segment:

    # def split_at_point:
