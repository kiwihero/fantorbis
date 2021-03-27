class VertexPoint:
    """
    A VertexPoint is a single point on a vertex dividing cells
    """
    def __init__(self):
        # TODO: Keeping track of & updating cells vs vertices, in one of the other
        self.cells = set()

    def neighboring_cells(self):
        """
        The cells surrounding each vertex
        :return: Set of cells surrounding a single point on a vertex
        """
        return self.cells
