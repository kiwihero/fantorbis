from PIL import Image, ImageDraw
import numbers

def show_world(world):
    canvas_width = 1200
    canvas_height = 800


    im = Image.new(mode="RGB", size=(canvas_width, canvas_height))
    draw = ImageDraw.Draw(im)
    struct = world.dataStructure

    if struct.cellShape == 'rectangle':

        locs = square_cells(im,struct)
        for row in locs:
            for col in row:
                draw.rectangle(col, fill=(100,100,100),
                               outline=None, width=0)
    else:
        return

    world.images[world.age] = im

def square_cells(image, rectanglestructure, sep_ratio=0.1, sep_fixed=None):
    square_dims = (int(image.size[0] / rectanglestructure.width), int(image.size[1] / rectanglestructure.height))

    separation = sep_fixed
    if separation == None:
        sep_type = None
        try:
            ratio_len = len(sep_ratio)
            # print("ratio len")
            if ratio_len > 1:
                sep_type = 'oversized'
            elif ratio_len == 1:
                sep_type = 'singleton'
            else:
                sep_ratio = [None,None]
        except TypeError:
            sep_ratio = [sep_ratio,sep_ratio]
        if sep_type == 'oversized':
            sep_ratio = [sep_ratio[0], sep_ratio[1]]
        elif sep_type == 'singleton':
            sep_ratio = [sep_ratio[0], sep_ratio[0]]

        try:
            sep_ratio_num = int(sep_ratio[0]) + int(sep_ratio[1])
            sep_type = 'num'
        except (ValueError, TypeError) as e:
            sep_ratio = [0, 0]

        square_dims = (
        int((image.size[0]) / ((rectanglestructure.width) + (rectanglestructure.width + 1) * sep_ratio[0])),
        int((image.size[1]) / ((rectanglestructure.height) + (rectanglestructure.height + 1) * sep_ratio[1])))
        separation = (
        int((image.size[0]-square_dims[0]*rectanglestructure.width)/(1+rectanglestructure.width)),
        int((image.size[1]-square_dims[1]*rectanglestructure.height)/(1+rectanglestructure.height)))

    else:
        try:
            if len(separation) > 2:
                separation = [separation[0],separation[1]]
            elif len(separation) == 1:
                separation = [separation[0], separation[0]]
        except TypeError: #if same sep given both dimensions, make array
            separation = [separation,separation]
            try:
                separation = [int(separation[0]) + 0,int(separation[1]) + 0]
            except (ValueError,TypeError):
                separation = [0,0]
        square_dims = (
        int((image.size[0]-((rectanglestructure.width+1)*separation[0])) / rectanglestructure.width),
        int((image.size[1]-((rectanglestructure.height+1)*separation[1])) / rectanglestructure.height))

    cell_locations = []

    y1=separation[1]
    y2=y1+square_dims[1]
    for h in range(rectanglestructure.height):
        location_row = []
        x1 = separation[0]
        x2 = x1 + square_dims[0]
        for w in range(rectanglestructure.width):
            location_row.append([x1,y1,x2,y2])
            x1 = x2 + separation[0]
            x2 += (separation[0] + square_dims[0])
        cell_locations.append(location_row)
        y1 = y2 + separation[1]
        y2 += (separation[1] + square_dims[1])

    print("square dims", square_dims, "separation", separation)
    print("cell locations",cell_locations)
    return cell_locations


