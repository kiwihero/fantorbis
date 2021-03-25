from backendworld.WorldAttribute import WorldAttribute

class TectonicCell(WorldAttribute):
    def __init__(self, **kwargs):
        self.age = 0
        self._dataStructureLocation = None
        super(TectonicCell, self).__init__(**kwargs)

    def move(self, dirx, diry):
        if self._dataStructureLocation is None:
            self.world.conf.log_from_conf('error', 'Cell is not associated with any data structure element')
        else:
            self.world._dataStructure.move_cell(self._dataStructureLocation, relative=(dirx,diry))


