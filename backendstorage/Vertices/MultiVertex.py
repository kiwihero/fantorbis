from backendstorage.Vertices.Vertex import Vertex


class MultiVertex(Vertex):
    def __init__(self, **kwargs):
        super(MultiVertex, self).__init__(**kwargs)

    # TODO: Needs functionality for branching vertices
    def add_vertex_segment(self, vertex_segment):
        """
        Extend an existing vertex using a vertex segment that connects
        :param vertex_segment: A single vertex segment that is contiguous with existing vertex
        :return: error if applicable
        """
        pass

