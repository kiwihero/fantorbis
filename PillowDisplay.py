from PIL import Image, ImageDraw, ImageFont
from PIL import ImageFont
import numbers
import os
import eris_gradient

# TODO: THIS FILE NEEDS DOCSTRINGS
#  Kitty doing this soon


def draw_world(world, add_text: bool =False):
    '''

    :param world: the World object that is being drawn.
    :param add_text: Boolean determining whether or not age should be written on the drawing.
    :return: he draws the world, however he does not show you the world. he draws it.
    '''
    canvas_width = world.conf.imageWidth
    canvas_height = world.conf.imageHeight


    im = Image.new(mode="RGB", size=(canvas_width, canvas_height))
    draw = ImageDraw.Draw(im)
    struct = world._dataStructure




    if struct.cellShape == 'rectangle':
        cellstruct = struct.CellStorage
        gradient_ends = world.conf.ageGradient
        gradient_steps = world.age+1
        full_gradient = eris_gradient.make_gradient(gradient_ends[0], gradient_ends[1], gradient_steps)
        print("full gradient len {}, contents {}".format(len(full_gradient), full_gradient))

        locs = _square_cells(im,cellstruct)
        r=0
        for row in locs:
            c = 0
            for col in row:
                ind_cell = cellstruct[r][c]
                ind_cell_age = ind_cell.worldCell.age
                # print("ind cell age {} type {}".format(ind_cell_age, type(ind_cell_age)))
                # print("ind cell age {}; color {}".format(ind_cell_age, full_gradient[ind_cell_age]))

                draw.rectangle(col, fill=full_gradient[ind_cell_age],
                               outline=None, width=0)
                c += 1
            r += 1
    else:
        world.conf.log_from_conf('error', "Cell shape not known, could not draw world")
        return

    world.images[world.age] = im

    if add_text is True:
        annotated_img = world.images[world.age].copy()
        annotated_draw = ImageDraw.Draw(annotated_img)
        caption = world.conf.imageCaption.format(world.age)
        _annotate_image(annotated_draw, caption=caption, position=world.conf.imageSmallCaptionPos, conf=world.conf)
        world.annotatedImages[world.age] = annotated_img

def image_world(world, force_current: bool =False, current_only: bool = False, image_type=('all', True)):
    '''

    :param world: World object
    :param force_current: determining if should include prevs or just current
    :param current_only: just current
    :param image_type: defines if you want annotated/unannotated, and if it should be forced
    :return: makes the image and plays with it. draw_world draws the image.
    '''
    valid_type_args = ['clean', 'annotated', 'all']
    try:
        if type(image_type) is str :
            raise CustomTypeError("Image_type requires two arguments and you gave the single string {}".format(image_type))
        if len(image_type) != 2:
            raise CustomTypeError("Image_type requires two arguments")
        if image_type[0] not in valid_type_args:
            raise CustomTypeError("Image type first argument \'{}\' invalid, must be in {}".format(image_type[0],valid_type_args))
        if type(image_type[1]) is not bool:
            raise CustomTypeError("Image type second argument \'{}\' invalid, must be a boolean".format(image_type[1]))
    except CustomTypeError as e:
        world.conf.log_from_conf('error', "{}, could not generate images for world".format(e.message))
        # print("Error {}, could not generate images for world".format(e.message))
        return
    type_mode = image_type[0]
    force_mode = image_type[1]

    image_dicts = {}
    image_dicts_len = 0
    if type_mode == 'clean':
        image_dicts['clean'] = world.images
        if force_mode != True:
            image_dicts['annotated'] = {}
            for age in world.annotatedImages:
                if age not in world.images:
                    image_dicts['annotated'][age] = world.annotatedImages[age]

    elif type_mode == 'annotated':
        image_dicts['annotated'] = world.annotatedImages
        if force_mode != True:
            image_dicts['clean'] = {}
            for age in world.images:
                if age not in world.annotatedImages:
                    image_dicts['clean'][age] = world.images[age]

    elif type_mode == 'all':
        image_dicts['clean'] = world.images
        image_dicts['annotated'] = world.annotatedImages



    for key,value in image_dicts.items():
        image_dicts_len += len(value)



    if image_dicts_len == 0:
        world.conf.log_from_conf('info', "No images already known")
        # print("no images already known")
        if world.age not in image_dicts['clean']:
            draw_world(world)
        if type_mode == 'annotated' or type_mode == 'all':
            annotated_img = world.images[world.age].copy()
            annotated_draw = ImageDraw.Draw(annotated_img)
            caption = world.conf.imageCaption.format(world.age)
            _annotate_image(annotated_draw,caption=caption, position=world.conf.imageSmallCaptionPos, conf=world.conf)
            world.annotatedImages[world.age] = annotated_img
            # print("annotated image", annotated_img)

    # else:
    #     print("Known image dicts", image_dicts)






    if (force_current is True) and (world.age not in world.images):
        draw_world(world)
    if current_only is True:
        age = world.age
        for key, value in image_dicts.items():
            im = value[age]
            filename = world.conf.imageName.format(key,str(age))
            _save_image(im, filename, world.conf)
    else:
        for key, value in image_dicts.items():
            # print("key {} value {}".format(key,value))
            for age, im in value.items():

                # print("age {} im {}".format(age, im))
                filename = world.conf.imageName.format(key,str(age))
                if '.' not in filename:
                    if '.' not in world.conf.defaultImageExtension:
                        filename += '.'
                    filename += world.conf.defaultImageExtension
                # print("Filename {} age {}".format(filename,age))
                _save_image(im, filename, world.conf)


def _save_image(image, filename, conf):

    '''

    :param image: the image being saved
    :param filename: where he is being saved to
    :param conf: directory
    :return: this function saves the image of the world
    '''
    # splitpath = filename.split()
    dirname = os.path.dirname(filename)
    # basnm = os.path.basename(filename)
    # print("splitpath {}, dirname {}, basename {}".format(splitpath,dirname, basnm))
    try:
        os.mkdir(dirname)
        conf.log_from_conf('info', "Had to create new directory {}".format(dirname))
        # print("new directory",dirname)
    except OSError as error:
        # print("existing directory",dirname)
        pass
    image.save(filename)





def gif_world(world):
    '''

    :param world: world object
    :return: this makes the world go weeee.
    '''
    if len(world.images) > 0:
        fnt = world.conf.fnt
        fnt_sm = world.conf.fnt_sm
        # ImageFont.truetype()
        images = []
        image_steps = list(world.images.keys()).copy()
        canvas_width = 0
        canvas_height = 0
        # gf = Image.new(mode="RGB")
        # print("image keys {}".format(image_steps))
        while len(image_steps) > 0:
            # min_step = image_steps.pop(min(image_steps))
            min_step = min(image_steps)
            image_steps.remove(min_step)
            next_img = world.images[min_step].copy()
            single_draw = ImageDraw.Draw(next_img)
            caption = world.conf.imageCaption.format(min_step)
            grayscale = 0.8
            _annotate_image(single_draw, position=world.conf.imageSmallCaptionPos, caption=caption,  conf=world.conf)
            world.annotatedImages[world.age] = next_img
            # annotate_image(single_draw, (20, 20), caption, anchor='lt', fill=(int(255 * grayscale), int(255 * grayscale), int(255 * grayscale), int(255 * grayscale)), stroke_width=1, font=fnt_sm)

            # single_draw.text((20,20), caption, anchor='lt', fill=(int(255*grayscale), int(255*grayscale), int(255*grayscale), int(255*grayscale)), stroke_width=1, font=fnt_sm)
            images.append(next_img)
            world.annotatedImages[min_step] = next_img
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
        # print("type {} {} rect {}".format(type(gf),type(draw), text_center))
        draw.text(text_center, reset_text, anchor='mb', fill=(255, 255, 255, 255), stroke_width=5,font=fnt)
        # draw.text(text_center, "->")
        text_center = (int(0.5 * canvas_width), int(0.75 * canvas_height))
        reset_text = "START ANEW"
        draw.text(text_center, reset_text, fill=(255, 255, 255, 255), stroke_width=5, anchor='mb',font=fnt)
        gf.save(world.conf.gifName, save_all=True, append_images=images[:], duration=world.conf.gifFrameDuration, loop=0)
        # print(type(w1.images))
        # (w1.images[max(w1.images.keys())]).show()

def _annotate_image(drawInstance, position, caption, conf):
    '''

    :param drawInstance: the instance chosen
    :param position: the xy coordinates
    :param caption: the text thats there
    :param conf: directory thing
    :return: puts text into an image
    '''
    # print("pos {} capt {}".format(position,caption))
    # drawInstance.text(xy=position, text=caption)
    drawInstance.text(xy=position, text=caption, anchor='lt',
                     fill=conf.imageAnnotationProperties['fill'],
                     stroke_width=conf.imageAnnotationProperties['stroke_width'], font=conf.imageAnnotationProperties['font'])




def _square_cells(image, rectanglestructure, sep_ratio=0.1, sep_fixed=None):

    '''

    :param image: world image working with
    :param rectanglestructure: rectangle
    :param sep_ratio: the ratio of seperation
    :param sep_fixed: the seperation of the rectangles
    :return: puts rectangles into square cells
    '''
    square_dims = (int(image.size[0] / rectanglestructure.cols), int(image.size[1] / rectanglestructure.rows))

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
        int((image.size[0]) / ((rectanglestructure.cols) + (rectanglestructure.cols + 1) * sep_ratio[0])),
        int((image.size[1]) / ((rectanglestructure.rows) + (rectanglestructure.rows + 1) * sep_ratio[1])))
        separation = (
        int((image.size[0]-square_dims[0]*rectanglestructure.cols)/(1+rectanglestructure.cols)),
        int((image.size[1]-square_dims[1]*rectanglestructure.rows)/(1+rectanglestructure.rows)))

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
    for h in range(rectanglestructure.rows):
        location_row = []
        x1 = separation[0]
        x2 = x1 + square_dims[0]
        for w in range(rectanglestructure.cols):
            location_row.append([x1,y1,x2,y2])
            x1 = x2 + separation[0]
            x2 += (separation[0] + square_dims[0])
        cell_locations.append(location_row)
        y1 = y2 + separation[1]
        y2 += (separation[1] + square_dims[1])

    print("square dims", square_dims, "separation", separation)
    print("cell locations",cell_locations)
    return cell_locations

class GenericError(Exception):
    pass

class CustomTypeError(GenericError):
    def __init__(self, message=None):
        self.message = message

