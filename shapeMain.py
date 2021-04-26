# from backendstorage.StorageMechanisms.ShapelyStructure import ShapelyStructure
from backendworld.World import World
from MatplotDisplay import plt_to_file

w1 = World()
print("World created {}".format(w1))
struct = w1.access_data_struct()
# plt_to_file(w1)
print("Shapely structure {}".format(struct))
w1.step()
struct.subdivide()
struct.update_cells()
w1.step()
# struct.subdivide()
# w1.step()
# struct.subdivide()
# w1.step()
# plt_to_file(w1)

#
# print("Shapely structure {}".format(struct.CellStorage))
# print("Shapely type {}".format(type(struct.CellStorage)))
#
# print("Shapely shpcell {}".format(struct.CellStorage['ShapelyCell']))
# print("Shapely shpcell type {}".format(type(struct.CellStorage['ShapelyCell'])))
# print("Cell was {}".format(struct.CellStorage['ShapelyCell'][0]))
# print("Cell polygon was {}".format(struct.CellStorage['ShapelyCell'][0].polygon))
# print("Column polygon was {}".format(struct.CellStorage['geometry'][0]))
# struct.CellStorage['ShapelyCell'][0].move(5,5)
# print("Cell now {}".format(struct.CellStorage['ShapelyCell'][0]))
# print("Cell polygon now {}".format(struct.CellStorage['ShapelyCell'][0].polygon))
# print("Column polygon now {}".format(struct.CellStorage['geometry'][0]))
# plt_to_file(w1)

struct.move_cell_in_structure('pos',0.1875,.25,.125)
w1.step()
for col in w1.conf.ShapelyStructureColumns:
    print("Column {}".format(col))
    print(struct.CellStorage[col])
struct.subdivide()
struct.update_cells()
w1.step()
struct.subdivide()
struct.update_cells()
w1.step()
print("Structure position points")

print(struct.CellStorage['pos_point'])
for i in range(len(struct.CellStorage)):
    matching_rows = struct.CellStorage.loc[struct.CellStorage['pos_point']== struct.CellStorage['pos_point'][i]]
    if len(matching_rows) > 1:
        print(struct.CellStorage['pos_point'][i])
        print("{} matching rows".format(len(matching_rows)))
        print(matching_rows)
plt_to_file(w1)