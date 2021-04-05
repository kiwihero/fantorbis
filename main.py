# from backendstorage.NodeStructure import *
from backendworld.World import *
from PillowDisplay import draw_world, gif_world,image_world, draw_detailed_step

#  THIS IS NOT A CALLABLE CLASS, THIS IS EXAMPLES DEMONSTRATING FUNCTIONALITY.
#  DO NOT CALL ANYTHING FROM HERE IN PRODUCTION.
#  ALL CONTENTS OF THIS FILE SUBJECT TO CHANGE AT ALL TIMES,
#  DO NOT EXPECT TO BE ABLE TO USE THIS

w1 = World()

print('\n'+'-'*50+'\n'+"PRINTING WORLD DATA STRUCTURE"+'\n')
print(type(w1._dataStructure),w1._dataStructure)
print('\n'+"DONE PRINTING WORLD DATA STRUCTURE"+'\n'+'-'*50)

print('\n'+'-'*50+'\n'+"PRINTING WORLD DATA STRUCTURE CONTENTS"+'\n')
print("data structure type {}".format(type(w1.access_data_struct())))
w1.access_data_struct().print_contents()
# w1._dataStructure.print_contents()
print('\n'+"DONE PRINTING WORLD DATA STRUCTURE CONTENTS"+'\n'+'-'*50)

# for elem in w1._dataStructure:
#     print("Elem",elem)
draw_world(w1, True)

w1.step()
actions = [{'function':'random_wiggle','class_instance':w1,'kwargs':{}}]
for x in range(2):
    draw_detailed_step(w1,actions)
draw_world(w1, True)

# for x in range(20):
#     # if x >=4:
#     #     break
#     if x % 3 == 0 and x < 10:
#         w1._dataStructure.subdivide()
#     else:
#         w1.random_wiggle()
#     draw_world(w1, True)
#     w1.step()
#
#     print("world cells count", len(w1.tectonicCells))
#     # print("images len {}, world age {}".format(len(w1.images),w1.age))


gif_world(w1)

image_world(w1)

# print("world", w1, "images", w1.images)

# if len(w1.images) > 0:
#     print(type(w1.images))
#     (w1.images[max(w1.images.keys())]).show()

for cell in w1.tectonicCells:
    print("cell age",cell.age)