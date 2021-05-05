import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.cm import ScalarMappable
from backendworld.pillowtime import pillow
import geopandas as gpd
from backendworld.World import World
from shapely.geometry.collection import GeometryCollection
from shapely.geometry.multipolygon import MultiPolygon
from shapely.geometry.polygon import Polygon
import pandas as pd

def draw_world(world, column='age_diff', force_draw:bool=False, hide_plates:bool=False, add_title:bool=True):
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
    gdf.boundary.plot(ax=ax, color='gray', zorder=6, alpha=0.5)
    if hide_plates is False:
        plate_boundaries.plot(ax=ax, color='purple', zorder=4, alpha=1)
        plates.plot(ax=ax, column='area', zorder=5, alpha=0.5)
    if column in world.conf.ShapelyStructureColumns:
        gdf.plot(column=column, ax=ax, legend=True)
        if add_title is True:
            plt.title(str(column))
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

def draw_plates(world, column='age_diff', force_draw:bool=False):
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
    # gdf = world.access_data_struct().CellStorage
    fig, ax = plt.subplots(1, 1)
    # gdf.boundary.plot(ax=ax, color='gray', zorder=6, alpha=0.5)
    plate_boundaries.plot(ax=ax, color='purple', zorder=4, alpha=1)
    plates.plot(ax=ax, column='area', zorder=5, alpha=0.5)
    # if column in world.conf.ShapelyStructureColumns:
        # gdf.plot(column=column, ax=ax, legend=True)
    # else:
        # raise Exception("Could not find the column {} in the dataframe to plot".format(column))
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

def plt_geoms(gdf, title=None, fill:bool=True):
    fig, ax = plt.subplots(1, 1)
    if type(gdf) is Polygon:
        gdf = [gdf]
    if type(gdf) is list:
        elem_count = 0
        colors=['black','red','blue','purple','green','yellow']
        for elem in gdf:
            # print('{} elem {}, geometry {}'.format(elem_count, type(elem),elem['geometry']))
            if type(elem) is MultiPolygon:
                elem = gpd.GeoDataFrame(list(elem))
                print('{} multipoly elem {}, geometry {}'.format(elem_count, type(elem), elem.geometry))
            if type(elem) is Polygon:
                elem_df = gpd.GeoDataFrame([elem])
                elem = elem_df.set_geometry([Polygon(elem.exterior.coords)])
                print('{} poly elem {}, geometry {}'.format(elem_count, type(elem), elem.geometry))
            if type(elem) is pd.Series:
                elem_df = elem.to_frame()
                elem_geom = gpd.GeoSeries(elem['geometry'].exterior)
                print("elem geom {}".format(elem_geom))
                # print('{} df elem {}, geometry\n{}\nend df elem'.format(elem_count, type(elem_df), elem_df))
                # elem_gdf = gpd.GeoDataFrame(elem_df, geometry=elem_geom)
                elem_gdf = elem_geom.to_frame()
                print('{} series elem {}'.format(elem_count, type(elem_gdf)))
                print('{} series elem {}'.format(elem_count, elem_gdf))
                print("cols {}".format(elem_gdf.columns))
                elem_gdf = elem_gdf.set_geometry([elem['geometry']])
                print('{} series elem {}'.format(elem_count, elem_gdf))
                print("cols {}".format(elem_gdf.columns))
                # elem_gdf.append(geometry=elem_df['geometry'])
                elem = elem_gdf
                print('{} series elem {}, geometry {}'.format(elem_count, type(elem), elem.geometry))
            elem.boundary.plot(ax=ax, color='gray', zorder=10)
            if fill is True:
                if 'color_scale' in elem.columns:
                    elem.plot(ax=ax, column='color_scale', legend=True,alpha=0.4,label=str(elem_count))
                elif elem_count < len(colors):
                    print("{} elements, set color {}".format(len(elem),colors[elem_count]))
                    elem.plot(ax=ax, legend=True, alpha=0.4, color=colors[elem_count],zorder=elem_count,label=str(elem_count))
                else:
                    elem.plot(ax=ax, legend=True,alpha=0.4,zorder=elem_count,label=str(elem_count))
            elem_count+= 1
    elif type(gdf) is MultiPolygon:
        poly_gdf = gpd.GeoDataFrame(list(gdf))
        plt_geoms(poly_gdf,title=title,fill=fill)
    else:
        print(gdf['geometry'])
        gdf.boundary.plot(ax=ax, color='gray', zorder=2)
        if fill is True:
            if 'color_scale' in gdf.columns:
                gdf.plot(ax=ax, column='color_scale',legend=True)
            elif 'given_color' in gdf.columns:
                gdf.plot(ax=ax, color='given_color', legend=True,alpha=0.4)
            else:
                gdf.plot(ax=ax, legend=True)
    if title is not None:
        plt.title(title)
    plt.show()

def plt_geom(poly, title=None):
    if type(poly) is GeometryCollection:
        return
    if type(poly) is gpd.GeoDataFrame:
        plt_geoms(poly)
    else:
        fig, ax = plt.subplots(1, 1)
        # gdf.exterior.plot(ax=ax, color='gray', zorder=2)
        if type(poly) is MultiPolygon:
            poly_gdf = gpd.GeoDataFrame(list(poly))
            print("poly_gdf {}".format(poly_gdf))
            plt_geoms(poly_gdf)
            return
            # raise Exception
        x, y = poly.exterior.xy
        plt.plot(x, y)
        # if 'color_scale' in gdf.columns:
        #     poly.plot(ax=ax, column='color_scale', legend=True)
        # else:
        #     poly.plot(ax=ax, legend=True)
        if title is not None:
            plt.title(title)
        plt.show()
