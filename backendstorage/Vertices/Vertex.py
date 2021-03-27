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
        if self.originVertexPoint is None and self.destinationVertexPoint is None:
            self.vertexSegments.add(vertex_segment)
            self.orderedVertexSegments.append(vertex_segment)
            return
        shared_points = {self.originVertexPoint, self.destinationVertexPoint} & vertex_segment.points()
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
                self.orderedVertexSegments.insert(0, vertex_segment)
            else:
                self.destinationVertexPoint = new_point
                self.orderedVertexSegments.append(vertex_segment)
            self.vertexSegments.add(vertex_segment)

    def remove_vertex_segment(self, vertex_segment):
        """
        Remove a vertex segment in the vertex
        Shorten vertex if possible
        Otherwise split into multiple segments
        :param vertex_segment: A single VertexSegment
        :return: Set of Vertex instances
        """
        if vertex_segment not in self.vertexSegments:
            return backendstorage.CustomExceptions.MessageError(
                "The segment {} could not be removed as it is not in the vertex {}".format(vertex_segment, self))
        segment_index = self.orderedVertexSegments.index(vertex_segment)
        shared_points = {self.originVertexPoint, self.destinationVertexPoint} & vertex_segment.points()
        if len(shared_points) == 0:
            return self.split_at_segment(vertex_segment)
        else:
            new_point = vertex_segment.points() - shared_points
            if len(new_point) == 0:  # segment of length 0 to be removed
                self.vertexSegments.remove(vertex_segment)
            if self.originVertexPoint in shared_points:
                self.originVertexPoint = new_point
            elif self.destinationVertexPoint in shared_points:
                self.destinationVertexPoint = new_point
            self.vertexSegments.remove(vertex_segment)
            self.orderedVertexSegments.pop(segment_index)
            return set(self)

    def split_at_segment(self, vertex_segment):
        segments = set()
        split_points = list(vertex_segment.points())
        split_vertex = self.split_at_point(split_points[0])
        for vertex in split_vertex:
            if vertex.is_contiguous(split_points[1]) == False:
                segments.add(vertex)
            else:
                new_vertex = new_vertex.split_at_point(split_points[1])
                segments.union(new_vertex)
        return segments

    def split_at_point(self, vertex_point):
        new_vertex = Vertex()
        segments = set()
        active_vertex = new_vertex
        for vertex_segment in self.orderedVertexSegments:
            if vertex_point in vertex_segment.points():
                segments.add(active_vertex)
                active_vertex = Vertex()
                segments.add(active_vertex)
            else:
                active_vertex.add_vertex_segment(vertex_segment)
        return segments



