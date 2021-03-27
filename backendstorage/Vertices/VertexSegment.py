from backendstorage.Vertices.VertexPoint import VertexPoint
import backendstorage.CustomExceptions
class VertexSegment:
    """
    A VertexSegment class instance is the line between two adjacent VertexPoints
    """
    def __init__(self, originPoint=None, destinationPoint=None):
        self._vertexOrigin = originPoint
        self._vertexDestination = destinationPoint
        self._vertexPoints = {self._vertexOrigin, self._vertexDestination}

    def remove_point(self, vertex_point):
        """
        Removes one of the points in the segment, creating a zero-length (origin = destination) segment
        :param vertex_point: Either a point in the segment, or string for origin or destination
        :return: the removed point
        """
        if vertex_point == 'origin' or vertex_point == 'o':
            return self.remove_point(self._vertexOrigin)
        if vertex_point == 'destination' or vertex_point == 'd':
            return self.remove_point(self._vertexDestination)
        if vertex_point not in self._vertexPoints:
            return backendstorage.CustomExceptions.MessageError(
                "The point {} is not in the segment {}".format(vertex_point, self))
        self._vertexPoints.remove(vertex_point)
        if vertex_point == self._vertexDestination:
            self._vertexDestination = None
            self.add_point(vertex_point)
        if vertex_point == self._vertexOrigin:
            self._vertexOrigin = None
            self.add_point(vertex_point)

    def add_point(self, vertex_point):
        """
        Adds a point to the segment end without a point
        :param vertex_point: The point to be added
        :return: error or new point
        """
        if self._vertexOrigin is None:
            self._vertexOrigin = vertex_point
        elif self._vertexDestination is None:
            self._vertexDestination = vertex_point
        else:
            return backendstorage.CustomExceptions.MessageError(
                "The point {} could not be added to the segment {} as it already has both an origin and a destination".format(
                    vertex_point, self))
        self._vertexPoints.add(vertex_point)
        return vertex_point

    def split_vertex(self):
        """
        If a VertexSegment's VertexPoints are no longer adjacent,
        it is necessary to split the VertexSegment into multiple VertexSegments
        :return: the set of VertexSegments that connects the original
        """
        # TODO: Ability to evaluate necessity of splitting, to allow multiple splits for one call
        new_vertex_point = VertexPoint()
        new_vertex_segment = self.insert_vertex(new_vertex_point)
        return new_vertex_segment

    def insert_vertex(self, new_vertex_point):
        """
        Splits a VertexSegment into two pieces, with a given VertexPoint as the split
        :param newVertexPoint: VertexPoint used to split the existing segment
        :return:
        """
        new_vertex_segment = VertexSegment(new_vertex_point, self._vertexDestination)
        self.remove_point(self._vertexDestination)

        return {self, new_vertex_segment}
