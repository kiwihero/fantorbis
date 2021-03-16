from backendstorage.GridStructure import *
from backendstorage.NodeStructure import *
from backendworld.World import *
from PillowDisplay import show_world

w1 = World()

print(type(w1.dataStructure),w1.dataStructure)

w1.dataStructure.print_contents()

show_world(w1)

print("world", w1, "images", w1.images)