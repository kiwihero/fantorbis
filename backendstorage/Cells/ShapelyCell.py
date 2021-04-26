from copy import copy, deepcopy
import geopandas as gpd
import pandas as pd
from shapely.geometry.polygon import Polygon
from shapely.affinity import affine_transform
from backendworld.TectonicCell import TectonicCell


class ShapelyCell:
    """
    Custom class extending a Shapely polygon
    """

    @property
    def exterior(self):
        return self.polygon.exterior

    @property
    def centroid(self):
        return self.polygon.centroid

    @property
    def bounds(self):
        return self.polygon.bounds

    @property
    def area(self):
        return self.polygon.area

    @property
    def length(self):
        return self.polygon.length

    @property
    def interiors(self):
        return self.polygon.interiors


    def __init__(self, conf=None, world_cell=None, world_cell_args: dict = None, cell_veolocity: float = 0, **kwargs):
        self.polygon = Polygon(**kwargs)
        print("ShapelyCell.polygon {} {}".format(type(self.polygon),self.polygon))
        # print("super polygon {}".format(super_polygon))
        # print("_geom {}".format(self.polygon._geom))
        # print("area {}".format(self.polygon.area))
        # print("exterior {}".format(self.polygon.exterior))
        # raise Exception
        # self.polygon = super().from_bounds(shell)
        # print("shapely cell geometry {}".format(self.BaseGeometry()))
        self.conf = conf
        self.velocity = cell_veolocity
        if world_cell_args is None:
            self.world_cell_args = {}
        else:
            self.world_cell_args = world_cell_args
        if world_cell is None:
            self.world_cell = TectonicCell()
        elif type(world_cell) is str:
            print("world cell input str")
            self.world_cell_class = conf.class_for_name(world_cell)
            self.world_cell = self.world_cell_class(**self.world_cell_args)
        else:
            self.world_cell_class = type(world_cell)
            self.world_cell = world_cell

    def subdivide(self):
        """
        Subdividing a single cell
        :return:
        """
        print("Starting subdivision on {}".format(self))
        new_polys = self._subdivide_square()
        # new_polys = self._subdivide_triangle()
        return new_polys
        # new_world_cell = copy(self.world_cell)
        # new_cell = ShapelyCell(
        #     self.conf, new_world_cell,self.world_cell_args)
        # print("made new cell {} using standard copy".format(new_cell))


        # new_cell.world_cell._dataStructureLocation = new_cell.dataStoragePosition
        # print("new world cell (id: {}) {}".format(hex(id(new_cell.worldCell)), new_cell.worldCell))
        # new_cell.worldCell.age = self.worldCell.age
        # new_cell.world_cell._updateWorldSet()

    def _subdivide_square(self):
        """
        Subdivision into four parts
        :return:
        """
        perim = self.exterior
        print("Perimeter",perim)
        # print("Perim coords",perim.coords)
        # print(len(perim.coords))
        # pts = gpd.GeoDataFrame(columns=['points'])
        # pts['points'] = pts.apply(lambda x: [y for y in self['geometry'].coords], axis=1)
        ctr = self.centroid

        print("centroid {} {}".format(type(ctr),ctr))
        points = []
        for i, p in enumerate(perim.coords):
            points.append(p)
        new_points = []
        for i in range(1,len(points)):
            midpoint = ((points[i-1][0]+points[i][0])/2,(points[i-1][1]+points[i][1])/2)
            print("midpoint {}".format(midpoint))
            print("\t{} {} {}".format(points[i-1],midpoint,points[i]))
            new_points.append(points[i-1])
            new_points.append(midpoint)
            # new_points.append(points[i])
        print("NEW POINTS")
        x = -1
        triples = []
        triple = []
        while x < len(new_points):
        # for x in range(-1,len(new_points)):

            print("\t{} {}".format(x, new_points[x]))
            triple.append(new_points[x])
            if len(triple) == 3:
                triple.append((ctr.x,ctr.y))
                triples.append(triple)
                triple = [new_points[x]]
            #     print("\t {} {}".format((x+2)%3,ctr))
            #     print("\t{} {}".format(x, new_points[x]))
            x+=1
        print("Triples")
        new_polys = gpd.GeoDataFrame(columns=self.conf.ShapelyStructureColumns)
        new_polys = []
        for trp in triples:
            new_poly = ShapelyCell(
                conf=self.conf, world_cell=self.world_cell, world_cell_args=self.world_cell_args, shell=trp
            )
            new_polys.append(new_poly._cell_to_structure_columns())
            print("new poly",new_poly)
            print(trp[0],trp[1],trp[2],trp[3])
        return new_polys

    def _subdivide_triangle(self):
        """
        Subdivision into four parts
        :return:
        """
        perim = self.exterior
        print("Perimeter",perim)
        # print("Perim coords",perim.coords)
        # print(len(perim.coords))
        # pts = gpd.GeoDataFrame(columns=['points'])
        # pts['points'] = pts.apply(lambda x: [y for y in self['geometry'].coords], axis=1)
        ctr = self.centroid

        print("centroid {} {}".format(type(ctr),ctr))
        points = []
        for i, p in enumerate(perim.coords):
            points.append(p)
        new_points = []
        midpoints = []
        for i in range(1,len(points)):
            midpoint = ((points[i-1][0]+points[i][0])/2,(points[i-1][1]+points[i][1])/2)
            print("midpoint {}".format(midpoint))
            print("\t{} {} {}".format(points[i-1],midpoint,points[i]))
            new_points.append(points[i-1])
            new_points.append(midpoint)
            midpoints.append(midpoint)
            # new_points.append(points[i])
        print("NEW POINTS")
        x = -1
        triples = [midpoints]
        triple = []
        while x < len(new_points):
        # for x in range(-1,len(new_points)):

            print("\t{} {}".format(x, new_points[x]))
            triple.append(new_points[x])
            if len(triple) == 3:
                # triple.append((ctr.x,ctr.y))
                triples.append(triple)
                triple = [new_points[x]]
            #     print("\t {} {}".format((x+2)%3,ctr))
            #     print("\t{} {}".format(x, new_points[x]))
            x+=1
        print("Triples")
        new_polys = gpd.GeoDataFrame(columns=self.conf.ShapelyStructureColumns)
        new_polys = []
        for trp in triples:
            new_poly = ShapelyCell(
                conf=self.conf, world_cell=self.world_cell, world_cell_args=self.world_cell_args, shell=trp
            )
            new_polys.append(new_poly._cell_to_structure_columns())
            print("new poly",new_poly)
            print(trp[0],trp[1],trp[2])
        return new_polys


    def _to_points(self, feature, poly):
        return {feature: poly.exterior.coords}

    def move(self, x_offset, y_offset):
        self.polygon = affine_transform(self.polygon, matrix=(1,0,0,1,x_offset,y_offset))

    def _cell_to_structure_columns(self):
        """
        Contains definitions for how to get the individual ShapelyCell value of each column of ShapelyStructure
        :return: Dictionary of columns and values used by ShapelyStructure
        """
        cell_value_templates = {
            'ShapelyCell':self,
            'TectonicCell':self.world_cell,
            'polygon':self.polygon,
            'geometry':self.polygon,
            'pos':self.centroid.x*self.centroid.y
        }
        requested_values = self.conf.ShapelyStructureColumns
        cell_values = dict()
        for column_name in requested_values:
            if column_name not in cell_value_templates:
                raise Exception("No known association between a ShapelyCell and the column {}".format(column_name))
            cell_values[column_name] = cell_value_templates[column_name]
        return cell_values

    def _cell_to_structure_df(self):
        cell_values = self._cell_to_structure_columns()
        for key, value in cell_values.items():
            cell_values[key] = [value]
        new_df = pd.DataFrame.from_dict(cell_values)
        print("New dataframe\n{}\nEnd new dataframe".format(new_df))
        return new_df
