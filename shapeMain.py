# from backendstorage.StorageMechanisms.ShapelyStructure import ShapelyStructure
from backendworld.World import World
from MatplotDisplay import plt_to_file

w1 = World()
print("World created {}".format(w1))
struct = w1.access_data_struct()
# plt_to_file(w1)
print("Shapely structure {}".format(struct))
struct.subdivide()
struct.subdivide()
struct.subdivide()
plt_to_file(w1)