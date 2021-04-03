from Position import Position

class Cell:
    """
    A single cell, surrounded by vertices
    """
    def __init__(self, conf=None, ds_pos=None, world_pos=None, world_cell=None, world_cell_args=None, **kwargs):
        print("initializing cell with args {} {} {} {} {}".format(ds_pos, world_pos,world_cell,world_cell_args, kwargs))
        self.conf = conf
        if ds_pos is None:
            if 'TwoDimensionalArray_pos' in kwargs:
                self.dataStoragePosition = kwargs['TwoDimensionalArray_pos']
            else:
                self.dataStoragePosition = Position()
        else:
            self.dataStoragePosition = ds_pos
        if world_pos is None:
            self.worldPosition = Position()
        else:
            self.worldPosition = world_pos
        # TODO: Keeping track of & updating cells vs vertices, in one of the other
        self.vertexPoints = set()
        if type(world_cell) is str:
            self.worldCell = conf.class_for_name(world_cell)(self.dataStoragePosition)
        else:
            self.worldCell = world_cell

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

    def __str__(self):
        if self.worldCell is not None:
            return "Cell at storage location {} has world cell {}".format(self.dataStoragePosition, self.worldCell)
        else:
            return "Cell at storage location {} has NO world cell".format(self.dataStoragePosition)
