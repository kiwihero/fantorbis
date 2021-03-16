from PIL import Image, ImageDraw

def show_world(world):
    canvas_width = 800
    canvas_height = 800

    im = Image.new(mode="RGB", size=(canvas_width, canvas_height))
    draw = ImageDraw.Draw(im)
    struct = world.dataStructure

    square_cells(im,struct)

    world.images[world.age] = im

def square_cells(image, rectanglestructure):
    pass