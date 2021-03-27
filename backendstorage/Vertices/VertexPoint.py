class VertexPoint:
    def __init__(self):
        # TODO: Keeping track of & updating cells vs vertices, in one of the other
        self.cells = set()

    def neighboring_cells(self):
        """
        The cells surrounding each vertex
        :return:
        """
        return self.cells
