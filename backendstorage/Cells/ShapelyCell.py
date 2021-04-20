from shapely.geometry.polygon import Polygon
from backendworld.TectonicCell import TectonicCell


class ShapelyCell(Polygon):
    """
    Custom class extending a Shapely polygon
    """
    def __init__(self, conf=None, world_cell: TectonicCell=None, world_cell_args=None, **kwargs):
        super(ShapelyCell, self).__init__(**kwargs)
        self.conf = conf
        if world_cell_args is None:
            self.world_cell_args = {}
        else:
            self.world_cell_args = world_cell_args
        if world_cell is None:
            self.world_cell = TectonicCell()
        elif type(world_cell) is str:
            self.world_cell_class = conf.class_for_name(world_cell)
            self.worldCell = self.world_cell_class(world=self.conf.world, **self.world_cell_args)
        else:
            self.world_cell_class = type(world_cell)
            self.worldCell = world_cell
