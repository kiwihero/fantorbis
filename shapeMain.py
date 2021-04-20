# from backendstorage.StorageMechanisms.ShapelyStructure import ShapelyStructure
from backendworld.World import World

w1 = World()
print("World created {}".format(w1))
struct = w1.access_data_struct()
print("Shapely structure {}".format(struct))
struct.subdivide()
struct.subdivide()