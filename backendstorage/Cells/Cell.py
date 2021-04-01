from Position import Position

class Cell:
    """
    A single cell, surrounded by vertices
    """
    def __init__(self, ds_pos=None, world_pos=None, **kwargs):
        if ds_pos is None:
            self.dataStoragePosition = Position()
        else:
            self.dataStoragePosition = ds_pos
        if world_pos is None:
            self.worldPosition = Position()
        else:
            self.worldPosition = world_pos
        # TODO: Keeping track of & updating cells vs vertices, in one of the other
        self.vertexPoints = set()
#         self._dataStorageStructure = None # should keep references to these???
#         self._worldStructure = None
#
    def move(self, newWorldPosition=None, newDataStoragePosition=None):
        """
        Change the position known by the cell in either world or data storage coordinate systems
        :param newWorldPosition: Position object
        :param newDataStoragePosition: Position object
        :return:
        """
        if newWorldPosition is not None:
            self.worldPosition.change_position(newWorldPosition)
        if newDataStoragePosition is not None:
            self.dataStoragePosition.change_position(newDataStoragePosition)
#
#     def splitCellAlongVertex(self, vertexSegment):
#         vertexSegment.splitVertex()
#
