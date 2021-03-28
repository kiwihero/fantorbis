from Position import Position

class Cell:
    def __init__(self):
        self.dataStoragePosition = Position()
        self.worldPosition = Position()
        self.vertexPoints = set()
#         self._dataStorageStructure = None
#         self._worldStructure = None
#
    def move(self, newWorldPosition=None, newDataStoragePosition=None):
        """
        Change the position known by the cell in either world or data storage coordinate systems
        :param newWorldPosition: (x,y
        :param newDataStoragePosition:
        :return:
        """
        if newWorldPosition is not None:
            self.worldPosition = newWorldPosition
        if newDataStoragePosition is not None:
            self.dataStoragePosition = newDataStoragePosition
#
#     def splitCellAlongVertex(self, vertexSegment):
#         vertexSegment.splitVertex()
#
