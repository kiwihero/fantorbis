from backendstorage.GridStructure import *
from backendstorage.NodeStructure import *
from backendworld.World import *
from PillowDisplay import show_world

w1 = World()

print(type(w1.dataStructure),w1.dataStructure)

w1.dataStructure.print_contents()

show_world(w1)

print("world", w1, "images", w1.images)

if len(w1.images) > 0:
    print(type(w1.images))
    (w1.images[max(w1.images.keys())]).show()