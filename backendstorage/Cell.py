class Cell:
    def __init__(self):
        self.dataStoragePosition = None
        self.worldPosition = None
        self.vertexPoints = set()
        self._dataStorageStructure = None
        self._worldStructure = None

    def move(self, newWorldPosition=None, newDataStoragePosition=None):
        if newWorldPosition is not None:
            self.worldPosition = newWorldPosition
        if newDataStoragePosition is not None:
            self.dataStoragePosition = newDataStoragePosition


