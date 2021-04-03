from backendworld.WorldAttribute import WorldAttribute

class TectonicCell(WorldAttribute):
    """
    A single cell of a standard size, making up a World
    """
    def __init__(self, **kwargs):
        self.age = 0
        self._dataStructureLocation = None
        super(TectonicCell, self).__init__(**kwargs)

    def step(self):
        """
        Single step through time
        :return:
        """
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
            self.world._dataStructure.move_cell(self._dataStructureLocation, relative=(dirx,diry))


