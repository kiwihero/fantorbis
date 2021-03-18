from backendstorage.GridStructure import *
from backendstorage.NodeStructure import *
from backendworld.World import *
from PillowDisplay import draw_world, gif_world

w1 = World()

print(type(w1.dataStructure),w1.dataStructure)

w1.dataStructure.print_contents()

for x in range(10):
    draw_world(w1)
    w1.step()
    print("images len {}, world age {}".format(len(w1.images),w1.age))


gif_world(w1)


# print("world", w1, "images", w1.images)
#
# if len(w1.images) > 0:
#     print(type(w1.images))
#     (w1.images[max(w1.images.keys())]).show()