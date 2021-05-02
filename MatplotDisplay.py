import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.cm import ScalarMappable
from backendworld.pillowtime import pillow

from backendworld.World import World

def draw_world(world, column='age_diff', force_draw:bool=False):
    """
    Draw the current world state as a PIL image, save it to the world
    The return is the dictionary entry that was added to world.images
    :param world: World object to be drawn
    :param column: Which column should be drawn
    :param force_draw: Force a redraw even if previously drawn
    :return: Dictionary of the age and the PIL image
    """
    plates = world.tectonicPlatesDf
    print("plates")
    print(plates)
    plate_boundaries = world.tectonicBoundariesDf
    print("plate boundaries")
    print(plate_boundaries)
    # raise Exception



    if force_draw is False and world.age in world.images and column in world.images[world.age]:
        return world.images[world.age][column]
    gdf = world.access_data_struct().CellStorage
    fig, ax = plt.subplots(1, 1)
    gdf.boundary.plot(ax=ax, color='gray', zorder=2)
    plate_boundaries.boundary.plot(ax=ax, color='black', zorder=4, alpha=0.5)
    plates.plot(ax=ax, color='pink', zorder=3, alpha=0.5)
    if column in world.conf.ShapelyStructureColumns:
        gdf.plot(column=column, ax=ax, legend=True)
    else:
        raise Exception("Could not find the column {} in the dataframe to plot".format(column))
    fig = plt.gcf()
    im = pillow(fig)
    if world.age not in world.images:
        world.images[world.age] = dict()
    world.images[world.age][column] = im
    # print("Output is type {}".format(type(im)))
    return world.images[world.age][column]
    # return {world.age: im}


def plt_to_file(world: World):
    gdf = world.access_data_struct().CellStorage
    print("gdf")
    print(gdf)

    plates = world.tectonicPlatesDf
    print("plates")
    print(plates)
    plate_boundaries = world.tectonicBoundariesDf
    print("plate boundaries")
    print(plate_boundaries)

    # print("geom")
    # print(gdf['geometry'].head(0))
    # print("end geom")
    fig, ax = plt.subplots(1, 1)
    gdf.boundary.plot(ax=ax,color='gray',zorder=2)
    gdf.plot(column='age_diff', ax=ax,legend=True)
    plate_boundaries.boundary.plot(ax=ax,color='black',zorder=4,alpha=0.5)
    plates.plot(ax=ax, color='pink', zorder=3, alpha=0.5)
    # col = gdf['age_diff']
    # print("col\n{}\nmin {} max {}".format(col, min(col),max(col)))
    # raise Exception



    # gdf.plot(column='stack_size', ax=ax)
    # gdf.plot(column='pos', ax=ax) #column='ShapelyCell'
    plt.savefig('pyplot_age')
    plt.show()
    fig, ax = plt.subplots(1, 1)
    gdf.boundary.plot(ax=ax, color='gray', zorder=2)
    gdf.plot(column='speed', ax=ax,legend=True)
    # fig.colorbar(ScalarMappable(), ax=ax)
    plt.savefig('pyplot_speed')
    plt.show()

def plt_geoms(gdf):
    fig, ax = plt.subplots(1, 1)
    print(gdf['geometry'])
    gdf.boundary.plot(ax=ax, color='gray', zorder=2)
    if 'color_scale' in gdf.columns:
        gdf.plot(ax=ax, column='color_scale',legend=True)
    else:
        gdf.plot(ax=ax, legend=True)
    plt.show()