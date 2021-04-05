# from backendworld.World import World
import random
from Position import Position
from copy import copy, deepcopy

class WorldAction():
    """
    Not a real class
    Holds functions for actions you can execute on the World
    Allows for more detailed logging of things done within a step
    """

    def __init__(self, world):
        self.world = world
        self.cells_altered = []
        self.cells_removed = []
        self.cells_added = []
        self.cell_movements = {}
        self.action_frames = {}

def random_wiggle_action(world):
    this_action = WorldAction(world)
    random_row = random.randint(0, world._dataStructure.height - 1)
    random_col = random.randint(0, world._dataStructure.width - 1)
    print(
        "world data structure {} type {} height {} type {} id {}".format(world._dataStructure, type(world._dataStructure),
                                                                         world._dataStructure.height,
                                                                         type(world._dataStructure.height),
                                                                         hex(id(world._dataStructure.height))))

    print("random row {}: {} max {}".format(type(random_row), random_row, world._dataStructure.height - 1))
    print("random col {}: {}".format(type(random_col), random_col))
    random_cell = world._dataStructure.CellStorage[random_row][random_col]
    this_action.cell_movements[random_cell] = [Position(int(random_cell.dataStoragePosition.x)+0,int(random_cell.dataStoragePosition.y)+0)]
    print("random cell {}: {}".format(type(random_cell), random_cell))
    print("cell movements ",str(this_action.cell_movements[random_cell][0]), hex(id(this_action.cell_movements[random_cell][0])))
    relx = random.randint(-1, 1)
    rely = random.randint(-1, 1)
    random_position = Position(relx, rely)
    destroyed_cell = world._dataStructure.CellStorage[random_position.y][random_position.x]
    this_action.cells_removed.append(destroyed_cell)
    this_action.cell_movements[destroyed_cell] = [copy(destroyed_cell.dataStoragePosition)]
    print("Moving random cell to {}".format(random_position))
    world._dataStructure.move_cell(random_cell, destination=random_position, relative=True)
    created_cell = world._dataStructure.CellStorage[random_cell.dataStoragePosition.y][random_cell.dataStoragePosition.x]
    this_action.cell_movements[created_cell] = [copy(created_cell.dataStoragePosition)]
    this_action.cells_added.append(created_cell)
    this_action.cells_altered.append(random_cell)
    this_action.cell_movements[random_cell].append(copy(random_cell.dataStoragePosition))
    print("cell movements 2", str(this_action.cell_movements[random_cell][0]),
          hex(id(this_action.cell_movements[random_cell][0])))
    print("cell movements 2", str(this_action.cell_movements[random_cell][1]),
          hex(id(this_action.cell_movements[random_cell][1])))
    print("New info for random cell {}".format(random_cell))
    # self._dataStructure.move_cell(random_cell, relative=(relx,rely))
    print("Altered cells {}\nCreated cells {}\nDestroyed cells {}".format(this_action.cells_altered,this_action.cells_added, this_action.cells_removed))
    for cell in this_action.cells_altered+this_action.cells_added+this_action.cells_removed:
        print("Affected cell", cell)
    print("Movements")
    for cell, mvmt in this_action.cell_movements.items():
        print("Cell: {}, movements: {}".format(cell,mvmt))
        for mv in mvmt:
            print("\t{}".format(mv))
    this_action.action_frames[0] = {"highlight": this_action.cell_movements[random_cell][0]}
    this_action.action_frames[1] = {"movement": this_action.cell_movements[random_cell]}
    this_action.action_frames[2] = {"highlight": this_action.cell_movements[random_cell][1]}
    return this_action