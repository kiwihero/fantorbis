from backendworld.WorldAttribute import WorldAttribute
from Position import Position
from Vector import Vector


class TectonicCell(WorldAttribute):
    """
    A single cell of a standard size, making up a World
    """
    def __init__(self, data_structure_location: Position = None, starting_height: int = 0, starting_velocity: Vector = None,
                 **kwargs):
        self.age = 0
        self.height = starting_height
        if starting_velocity is None:
            self.velocity = Vector(Position(0,0),Position(0,0))
        else:
            self.velocity = starting_velocity
        self._dataStructureLocation = data_structure_location
        super(TectonicCell, self).__init__(**kwargs)
        self._updateWorldSet()

    def _updateWorldSet(self):
        """
        Helper function to check if self is in world's list of TectonicCell
        :return:
        """
        if (self.world is not None) and (self not in self.world.tectonicCells):
            print("cell {} had to be added to world's known".format(self))
            self.world.tectonicCells.add(self)
        elif self.world is None:
            print("ERROR NO WORLD")

    def step(self):
        """
        Single step through time
        Also double checks if in world's set of known cells
        :return:
        """
        self._updateWorldSet()
        if self.velocity.magnitude() > 0:
            print("CELL HAS EXISTING VELOCITY {}".format(self.velocity))
            self.move(self.velocity.x_component(),self.velocity.y_component())
        if self.age == self.world.age:
            if self.world is not None:
                self.world.conf.log_from_conf(level="error", message="ONE CELL (ID: {}) CAN'T BE OLDER THAN THE WORLD".format(hex(id(self))))
            else:
                print("ONE CELL (ID: {}) CAN'T BE OLDER THAN THE WORLD\nAND TO TOP IT OFF, YOU NEVER GAVE YOUR CELLS A WORLD FOR THIS MESSAGE TO BE LOGGED".format(hex(id(self))))
                raise Exception
                # TODO: Can a bit of world be older than the world? Meteors??? Creationists???
        else:
            self.age += 1

    def move(self, dirx, diry):
        """
        Move cell within world a relative amount
        Requires TectonicCell to have an associated data structure to define movement,
        as actual functionality is in there not here
        :param dirx: Amount of x-direction movement requested
        :param diry: Amount of y-direction movement requested
        :return:
        """
        if self._dataStructureLocation is None:
            self.world.conf.log_from_conf('error', 'Cell is not associated with any data structure element')
        else:
            new_pos = Position(dirx, diry)
            print("self._dataStructureLocation",self._dataStructureLocation)
            self.world._dataStructure.move_cell(self._dataStructureLocation, destination=new_pos, relative=True)
            # raise Exception

    def __str__(self):
        return "Tectonic cell age {}; {} in data structure".format(self.age, self._dataStructureLocation)

    def __copy__(self):
        new_cell = TectonicCell(data_structure_location=self._dataStructureLocation, world=self.world)
        # new_cell = self.copy_attrs(new_cell)
        new_cell.age = self.age
        print("updating after copy, new cell world now {}".format(new_cell.world))
        new_cell._updateWorldSet()
        print("done updating after copy")
        return new_cell



