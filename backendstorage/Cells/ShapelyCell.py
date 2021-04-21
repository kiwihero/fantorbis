from copy import copy, deepcopy
import geopandas as gpd
from shapely.geometry.polygon import Polygon
from backendworld.TectonicCell import TectonicCell


class ShapelyCell(Polygon):
    """
    Custom class extending a Shapely polygon
    """

    def __init__(self, conf=None, world_cell=None, world_cell_args: dict = None, **kwargs):
        super(ShapelyCell, self).__init__(**kwargs)
        # print("shapely cell geometry {}".format(self.BaseGeometry()))
        self.conf = conf
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
        new_polys = gpd.GeoDataFrame(columns=['ShapelyCell', 'TectonicCell','geometry','pos'])
        new_polys = []
        for trp in triples:
            new_poly = ShapelyCell(
                conf=self.conf, world_cell=self.world_cell, world_cell_args=self.world_cell_args, shell=trp
            )
            new_polys.append({
                'ShapelyCell': new_poly,
                'TectonicCell': new_poly.world_cell,
                'geometry': self,
                'pos': new_poly.centroid.x*new_poly.centroid.y
            })
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
            if len(triple) == 2:
                triple.append((ctr.x,ctr.y))
                triples.append(triple)
                triple = [new_points[x]]
            #     print("\t {} {}".format((x+2)%3,ctr))
            #     print("\t{} {}".format(x, new_points[x]))
            x+=1
        print("Triples")
        new_polys = gpd.GeoDataFrame(columns=['ShapelyCell', 'TectonicCell', 'geometry', 'pos'])
        new_polys = []
        for trp in triples:
            new_poly = ShapelyCell(
                conf=self.conf, world_cell=self.world_cell, world_cell_args=self.world_cell_args, shell=trp
            )
            new_polys.append({
                'ShapelyCell': new_poly,
                'TectonicCell': new_poly.world_cell,
                'geometry': self,
                'pos': new_poly.centroid.x*new_poly.centroid.y
            })
            print("new poly",new_poly)
            print(trp[0],trp[1],trp[2])
        return new_polys


    def _to_points(self, feature, poly):
        return {feature: poly.exterior.coords}

