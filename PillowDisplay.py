from PIL import Image, ImageDraw, ImageFont
from PIL import ImageFont
import numbers


def draw_world(world):
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

def gif_world(world):
    if len(world.images) > 0:
        fnt = ImageFont.truetype(world.conf.fontLocation,100)
        fnt_sm = ImageFont.truetype(world.conf.fontLocation, 20)
        # ImageFont.truetype()
        images = []
        image_steps = list(world.images.keys())
        canvas_width = 0
        canvas_height = 0
        # gf = Image.new(mode="RGB")
        print("image keys {}".format(image_steps))
        while len(image_steps) > 0:
            # min_step = image_steps.pop(min(image_steps))
            min_step = min(image_steps)
            image_steps.remove(min_step)
            next_img = world.images[min_step]
            single_draw = ImageDraw.Draw(next_img)
            caption = "Age: {}".format(min_step)
            grayscale = 0.8
            single_draw.text((20,20), caption, anchor='lt', fill=(int(255*grayscale), int(255*grayscale), int(255*grayscale), int(255*grayscale)), stroke_width=1, font=fnt_sm)
            images.append(next_img)
            if world.images[min_step].size[0] > canvas_width:
                canvas_width = world.images[min_step].size[0]
            if world.images[min_step].size[1] > canvas_height:
                canvas_height = world.images[min_step].size[1]
            # print("min key {}, value {}".format(min_step, world.images[min_step]))

        # gf = Image.new(mode=images[0].mode, size=(canvas_width,canvas_height))
        gf = images[0]
        draw = ImageDraw.Draw(gf)
        # draw_rect = (int(0.25*canvas_width),int(0.25*canvas_height),int(0.75*canvas_width),int(0.75*canvas_height))
        text_center = (int(0.5 * canvas_width), int(0.25 * canvas_height))
        reset_text = "END OF WORLD"
        print("type {} {} rect {}".format(type(gf),type(draw), text_center))
        draw.text(text_center, reset_text, anchor='mb', fill=(255, 255, 255, 255), stroke_width=5,font=fnt)
        # draw.text(text_center, "->")
        text_center = (int(0.5 * canvas_width), int(0.75 * canvas_height))
        reset_text = "START ANEW"
        draw.text(text_center, reset_text, fill=(255, 255, 255, 255), stroke_width=5, anchor='mb',font=fnt)
        gf.save('out.gif', save_all=True, append_images=images[:], duration=200, loop=0)
        # print(type(w1.images))
        # (w1.images[max(w1.images.keys())]).show()

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


