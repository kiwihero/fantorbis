import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.cm import ScalarMappable

from backendworld.World import World

def plt_to_file(world: World):
    gdf = world.access_data_struct().CellStorage
    print("gdf")
    print(gdf)
    # print("geom")
    # print(gdf['geometry'].head(0))
    # print("end geom")
    fig, ax = plt.subplots(1, 1)
    gdf.boundary.plot(ax=ax,color='gray',zorder=2)
    gdf.plot(column='age_diff', ax=ax,legend=True)
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