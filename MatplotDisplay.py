import matplotlib.pyplot as plt

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
    gdf.plot(column='stack_size', ax=ax)
    # gdf.plot(column='pos', ax=ax) #column='ShapelyCell'
    plt.savefig('pyplot')
    plt.show()
