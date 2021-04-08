from Position import Position
import copy
# from copy import copy, deepcopy

class Cell:
    """
    A single cell, surrounded by vertices
    """
    def __init__(self, conf=None, ds_pos=None, world_pos=None, world_cell=None, world_cell_args=None, ds_holder=None, **kwargs):
        outstr = ("initializing cell with args (conf={}) (ds_pos={}) (world_pos={}) (world_cell={}) (world_cell_args={}) and {} kwargs:\n".format(conf, ds_pos, world_pos,world_cell,world_cell_args, len(kwargs)))
        for key, value in kwargs.items():
            if key == 'parent' and value is not None:
                # outstr += "({}) {}: ({}) \n{}\n".format(type(key), key, type(value), value.return_contents())
                outstr += "({}) {}: ({})\n".format(type(key), key, type(value))
            else:
                outstr += "({}) {}: ({}) {}\n".format(type(key),key, type(value), value)
        print(outstr)
        self.conf = conf
        if 'TwoDimensionalArray_pos' in kwargs:
            # print("Given 2darray pos", kwargs['TwoDimensionalArray_pos'])
            self.dataStoragePosition = kwargs['TwoDimensionalArray_pos']
        elif ds_pos is None:
            # print("No ds_pos given")
            self.dataStoragePosition = Position()
        else:
            # print("Known ds pos", ds_pos)
            self.dataStoragePosition = ds_pos
        if world_pos is None:
            self.worldPosition = Position()
        else:
            self.worldPosition = world_pos
        if world_cell_args is None:
            self.world_cell_args = {}
        else:
            self.world_cell_args = world_cell_args
        self.dataStorageContainer = ds_holder
        print("world cell args", self.world_cell_args)
        # self.world_cell_args['data_structure_location'] = self.dataStoragePosition
        # TODO: Keeping track of & updating cells vs vertices, in one of the other
        self.vertexPoints = set()
        if type(world_cell) is str:
            self.world_cell_class = conf.class_for_name(world_cell)
            self.worldCell = self.world_cell_class(self.dataStoragePosition, world=self.conf.world, **self.world_cell_args)
        else:
            self.world_cell_class = type(world_cell)
            self.worldCell = world_cell
        print("(cell id: {}) Cell {} has world cell STARTWORLDCELL {} ENDWORLDCELL (worldcell id: {}) WORLD {}".format(hex(id(self)),self, self.worldCell, hex(id(self.worldCell)), self.worldCell.world))


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
            self.dataStoragePosition.change_position(newDataStoragePosition, wrap_x=self.dataStorageContainer.width, wrap_y=self.dataStorageContainer.height)

    def __str__(self):
        if self.worldCell is not None:
            return "(cell id {}) Cell at storage location {} has world cell (id {}) {}".format(hex(id(self)),self.dataStoragePosition, hex(id(self.worldCell)), self.worldCell)
        else:
            return "(cell id {}) Cell at storage location {} has NO world cell".format(hex(id(self)),self.dataStoragePosition)

    def copy(self, copy_method: str = None, **kwargs):
        """
        Used to copy some elements and not others, to enable proper subdivision
        :return:
        """
        print("Copying Cell with method {}".format(copy_method))
        if copy_method is None:
            new_cell = Cell(conf=self.conf, ds_pos=self.dataStoragePosition,world_pos=self.worldPosition,world_cell=self.worldCell,world_cell_args=self.world_cell_args)
            # del copy
            # new_cell = copy(self)
            return new_cell
        elif copy_method == 'subdivision':
            # TODO:
            #  This can only handle if intial cell was created by defining class of TectonicCell
            #  It needs to handle finding class if instance is given
            new_cell = self.copy()
            print("made new cell {} using standard copy".format(new_cell))
            print("default world cell {}".format(new_cell.worldCell))
            print("old world cell (id: {}) {}".format(hex(id(self.worldCell)),self.worldCell))
            new_cell.worldCell = copy.copy(self.worldCell)
            new_cell.worldCell._dataStructureLocation = new_cell.dataStoragePosition
            print("new world cell (id: {}) {}".format(hex(id(new_cell.worldCell)),new_cell.worldCell))
            # new_cell.worldCell.age = self.worldCell.age
            new_cell.worldCell._updateWorldSet()
            # new_cell.worldCell._dataStructureLocation = copy.copy(self.worldCell._dataStructureLocation)
            # if type(self.world_cell_class) is str:
            #     new_cell.worldCell = self.conf.class_for_name(self.world_cell_class_str)(self.dataStoragePosition, world=self.conf.world,world_cell_args=self.world_cell_args)
            # if type(self.world_cell_class) is None:
            #     print("knwonw world cell {}".format(self.worldCell))
            #     raise Exception
            # else:
            #     new_cell.worldCell = self.world_cell_class(self.dataStoragePosition, world=self.conf.world,**self.world_cell_args)
            # print("subdivision copying made {}".format(new_cell))
            return new_cell
        else:
            # TODO: Error handling if unknown copy method
            # working on this - Vito
            raise Exception
