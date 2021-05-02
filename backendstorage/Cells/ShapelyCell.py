from copy import copy, deepcopy
import geopandas as gpd
import pandas as pd
from shapely.geometry.polygon import Polygon, LineString, LinearRing
from shapely.geometry.multipolygon import MultiPolygon
from shapely.geometry.point import Point
from shapely.geometry.linestring import LineString
from shapely.affinity import affine_transform, skew, scale
from backendworld.TectonicCell import TectonicCell
import copy
import math

from MatplotDisplay import plt_geoms


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

    @property
    def speed(self):
        return self.calculate_speed()

    @property
    def x_size(self):
        return self.bounds[2]-self.bounds[0]

    @property
    def y_size(self):
        return self.bounds[3]-self.bounds[1]


    def __init__(self, conf=None, age=None, world_cell=None, world_cell_args: dict = None, cell_veolocity=None, **kwargs):
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
        if age is None:
            self.creation_age = int(self.conf.world.age)
        else:
            self.creation_age = int(age)
        self.creation_age_list = [self.creation_age]
        if cell_veolocity is None:
            self.velocity = LineString([(0, 0), (0, 0)])
        else:
            # TODO: Handle velocities not centered on cell
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
            print("world cell args {}".format(self.world_cell_args))
        else:
            self.world_cell_class = type(world_cell)
            self.world_cell = world_cell
        self.world_cell.age = self.creation_age
        self.last_skew_path = gpd.GeoDataFrame(columns=['geometry'])

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
            new_world_cell = copy.deepcopy(self.world_cell)
            new_poly = ShapelyCell(
                conf=self.conf, world_cell=copy.deepcopy(self.world_cell), world_cell_args=self.world_cell_args,
                shell=trp, cell_veolocity=self.velocity,age=self.creation_age
            )
            # TODO: Remove purged cells from World's tectonic cell list
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
                conf=self.conf, world_cell=copy.deepcopy(self.world_cell), world_cell_args=self.world_cell_args,
                shell=trp, cell_veolocity=self.velocity, age=self.creation_age
            )
            # TODO: Remove purged cells from World's tectonic cell list
            new_polys.append(new_poly._cell_to_structure_columns())
            print("new poly",new_poly)
            print(trp[0],trp[1],trp[2])
        return new_polys


    def _to_points(self, feature, poly):
        return {feature: poly.exterior.coords}

    def move(self, x_offset, y_offset, change_velocity: bool = False, velocity_offset = None):
        """
        NOTE THAT IF THE SQRT(XOFFSET^2+YOFFSET^2) IS LESS THAN MU OF WORLD_CELL, CELL STOPS MOVING ALTOGETHER
        :param x_offset:
        :param y_offset:
        :param change_velocity:
        :param velocity_offset:
        :return:
        """
        print("Called ShapelyCell.move() on the cell {}".format(self))
        old_pos = Point(self.centroid)
        old_vel = LineString(self.velocity)
        print("old position {} {} {}".format(old_pos,old_pos.coords.xy,old_pos.coords.xy[0]))
        old_bounds = LinearRing(self.exterior)
        old_polygon = Polygon(self.polygon)
        print("old velocity {}".format(old_vel))

        self.polygon = affine_transform(self.polygon, matrix=(1, 0, 0, 1, x_offset, y_offset))
        new_pos = self.centroid
        print("new position {}".format(new_pos))
        pos_chg = LineString([old_pos,new_pos])
        old_offset_polygon = Polygon(old_polygon)
        new_offset_polygon = Polygon(self.polygon)
        if change_velocity is True:
            pos_vel_chg = pos_chg
            vel_chg = []
            print("position change {}".format(pos_chg))
            print("old vel coords {}: {}".format(type(old_vel.coords), old_vel.coords))
            for coord in range(min(len(old_vel.coords), len(pos_vel_chg.coords))):
                print("{} old vel = {}, pos chg = {}".format(coord, old_vel.coords[coord], pos_vel_chg.coords[coord]))
                vel_chg.append((old_vel.coords[coord][0] + pos_vel_chg.coords[coord][0],
                                old_vel.coords[coord][1] + pos_vel_chg.coords[coord][1]))
            print("vel chg {}".format(vel_chg))
            vel_x = vel_chg[1][0] - vel_chg[0][0]
            vel_y = vel_chg[1][1] - vel_chg[0][1]
            print("vel x {}, y {}".format(vel_x, vel_y))
            cell_mu = self.world_cell.mu
            print("cell mu {}".format(cell_mu))
            if abs(math.sqrt(math.pow(vel_x,2)+math.pow(vel_y,2))) < cell_mu:
                self.polygon = old_polygon
                self.velocity = LineString([(0, 0), (0, 0)])
                print("U gotta stop, u can't go so slow. U now moving at {}".format(self.velocity))
                print("U got reset back to centroid {}".format(self.centroid))
                # raise Exception
                return self
            if velocity_offset is not None:
                print("velocity offset {}".format(velocity_offset))
                print("old vel chg {}".format(vel_chg))
                new_vel_chg = [
                    (vel_chg[0][0]+velocity_offset[0],vel_chg[0][1]+velocity_offset[1]),
                    (vel_chg[1][0], vel_chg[1][1])
                    ]
                print("new vel chg {}".format(new_vel_chg))
                vel_chg = new_vel_chg
                print("old polygon {}".format(old_offset_polygon))
                print("new polygon {}".format(new_offset_polygon))
                old_offset_polygon = affine_transform(old_offset_polygon, matrix=(1, 0, 0, 1, velocity_offset[0], velocity_offset[1]))
                new_offset_polygon = affine_transform(new_offset_polygon, matrix=(1, 0, 0, 1, -1*velocity_offset[0], -1*velocity_offset[1]))
                print("old offset polygon {}".format(old_offset_polygon))
                print("new offset polygon {}".format(new_offset_polygon))
                # raise Exception
            # if abs(vel_chg[0][1] - vel_chg[1][1]) >= 0.5 or abs(vel_chg[0][0] - vel_chg[1][0]) >= 0.5:
            #     print("Vel chg {}".format(vel_chg))
            #     raise Exception
            new_vel = LineString(vel_chg)
            print("New velocity {}".format(new_vel))
            new_vel = scale(new_vel, 1-cell_mu, 1-cell_mu, origin=new_vel.coords[0])
            print("After friction velocity {}".format(new_vel))
            # raise Exception



            print("new velocity {}".format(new_vel))
            print("velocity change {}".format(vel_chg))
            self.velocity = new_vel
            print("offsets {}, {}".format(x_offset, y_offset))
            old_multi_polys = MultiPolygon([self.polygon, old_offset_polygon])
            new_multi_polys = MultiPolygon([new_offset_polygon, old_polygon])
            old_min_rot = old_multi_polys.minimum_rotated_rectangle
            new_min_rot = new_multi_polys.minimum_rotated_rectangle
            old_min_env = old_multi_polys.envelope
            new_min_env = new_multi_polys.envelope
            old_min_around = old_min_rot.intersection(old_min_env)
            new_min_around = new_min_rot.intersection(new_min_env)
            print("minimum around {}, {}".format(old_min_around,new_min_around))
            min_rot_df = gpd.GeoDataFrame([[old_min_around], [new_min_around], [self.polygon], [old_polygon]], columns=['geometry'])
            new_min_rot_df = gpd.GeoDataFrame([[new_min_around], [old_polygon], [new_offset_polygon]], columns=['geometry'])
            old_min_rot_df = gpd.GeoDataFrame([[old_min_around], [old_offset_polygon], [self.polygon]], columns=['geometry'])
            skew_positions = gpd.GeoDataFrame([[new_min_around], [old_min_around]], columns=['geometry'])
            self.last_skew_path = skew_positions

            skewed_pos = self.skew(old_polygon, x_offset + self.x_size, y_offset + self.y_size)

            skewed_pos = skewed_pos.append({'geometry': self.polygon, 'color_scale': 3}, ignore_index=True)
            # plt_geoms(min_rot_df)
            # plt_geoms(new_min_rot_df)
            # plt_geoms(old_min_rot_df)
            # plt_geoms(skewed_pos)




        return self

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
            'pos':self.centroid.x*self.centroid.y,
            'age_diff': sum(self.creation_age_list)/len(self.creation_age_list),
            # 'age_diff': self.world_cell.age,
            # 'age_diff': self.creation_age,
            # 'age_diff':self.conf.world.age-self.world_cell.age,
            'pos_point':self.centroid,
            'stack_size':self.world_cell.stack_size,
            'speed':self.speed
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

    def update_structure(self,containing_structure):
        print("Initial structure\n{}\nEnd initial structure".format(containing_structure))
        new_dataframe = self._cell_to_structure_df()
        altered_structure = containing_structure.append(new_dataframe)
        print("Altered structure\n{}\nEnd altered structure".format(containing_structure))
        matching_rows = containing_structure.loc[containing_structure['pos_point'] == self.centroid]
        if len(matching_rows) > 0:
            print("Multiple rows")
            raise Exception
        return altered_structure

    def join_cells(self, additional_cells):
        # print("Joining cells \n{}\nend cells\nto cell\n{}\nend cell".format(additional_cells,self))
        world = self.world_cell.world
        # print("world {}".format(world))
        # print("old world cell {}".format(self.world_cell))
        velocity_sum = [
            [
                self.velocity.coords[0][0]*self.world_cell.stack_size,
                self.velocity.coords[0][1]*self.world_cell.stack_size
            ],
            [
                self.velocity.coords[1][0]*self.world_cell.stack_size,
                self.velocity.coords[1][1]*self.world_cell.stack_size
            ]
        ]
        uneven_velocities = False
        mass_sum = self.world_cell.stack_size
        for cell in additional_cells:
            self.creation_age_list += cell.creation_age_list
            for pt in range(min(len(self.velocity.coords),len(cell.velocity.coords))):
                velocity_sum[pt][0] += cell.velocity.coords[pt][0]*cell.world_cell.stack_size
                velocity_sum[pt][1] += cell.velocity.coords[pt][1]*cell.world_cell.stack_size
                print("pt {} = {}".format(pt,velocity_sum[pt]))
                mass_sum += cell.world_cell.stack_size
            if self.velocity != cell.velocity:
                print("Uneven velocities {}, {}".format(self.velocity, cell.velocity))
                print("velocity sum {}".format(velocity_sum))
                uneven_velocities = True
                # raise Exception
            self.world_cell = world.converge_cells(self.world_cell,cell.world_cell)
            cell.world_cell = self.world_cell
        #TODO: Remove purged cells from World's tectonic cell list

        if uneven_velocities == True:
            new_vel_points = []
            for pt in range(len(velocity_sum)):
                velocity_sum[pt][0] /= ((1 + len(additional_cells))*mass_sum)
                velocity_sum[pt][1] /= ((1 + len(additional_cells))*mass_sum)
                new_vel_points.append((velocity_sum[pt][0],velocity_sum[pt][1]))

            # print("New velocity {}".format(velocity_sum))
            # print("New velocity points {} {}".format(new_vel_points,LineString(new_vel_points)))
            self.velocity = LineString(new_vel_points)
            # print("new velocity attribute {}".format(self.velocity))
            # raise Exception


        # print("new world cells\n{}\n{}\nEnd new world cells".format(self.world_cell,cell.world_cell))
        #
        # print("new world cell ids\n{}\n{}\nEnd new world cell ids".format(hex(id(self.world_cell)),hex(id(cell.world_cell))))

            # print("\tadditional cell {}".format(cell))
        return self._cell_to_structure_df()

    def calculate_speed(self):
        print("Velocity {} = speed {}".format(self.velocity, self.velocity.length))
        return self.velocity.length

    def skew(self,poly,dx,dy):
        print("dx {}, dy {}".format(dx,dy))
        print("skewing polygon {}".format(poly))
        skewed_poly = affine_transform(poly,[1,dx,dy,1,0,0])
        # skewed_poly_y = affine_transform(skewed_poly_x,[1,0,dy,1,0,0])
        new_skew_poly = skewed_poly.difference(poly)
        print("skewed polygon {}".format(skewed_poly))
        skewed_gdf = gpd.GeoDataFrame([[poly,1],[skewed_poly,2]],columns=['geometry','color_scale'])
        # skewed_gdf = gpd.GeoDataFrame([[new_skew_poly, 2]], columns=['geometry', 'color_scale'])

        return skewed_gdf

