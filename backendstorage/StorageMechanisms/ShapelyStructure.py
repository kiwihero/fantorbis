import geopandas as gpd
import pandas as pd
import math
import copy
import random
from shapely.geometry.linestring import LineString
from shapely.geometry.point import Point
from shapely.geometry.polygon import Polygon
from shapely.ops import unary_union
from shapely.geometry.collection import GeometryCollection

from backendstorage.StorageMechanisms.ArrayStructure import *
from backendstorage.Cells.ShapelyCell import ShapelyCell
from MatplotDisplay import plt_geoms, plt_geom


class ShapelyStructure(ArrayStructure):
    """
    Not a real structure either, don't use this itself
    Structures that use arrays instead of pointers to hold information
    """
    def __init__(self, wrap: bool = True, default_size=2, **kwargs):
        """
        This is an actual structure
        :param kwargs:
        """
        super(ShapelyStructure, self).__init__(**kwargs)
        self.world = self.conf.world
        first_cell = ShapelyCell(
            conf=self.conf,
            shell=[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]],
            # shell=[[0, 0], [0, 1], [math.sqrt(3)/2, .5], [0, 0]],
            world_cell_args=dict([('world', self.conf.world)]),
            world_cell='TectonicCell'
        )
        self.CellStorage = gpd.GeoDataFrame(columns=self.conf.ShapelyStructureColumns)
        self.wrap = wrap
        self.bounds = first_cell.bounds
        # gpd.GeoDataFrame(
        #     [[
        #         first_cell,
        #         first_cell.world_cell,
        #         first_cell,
        #         first_cell.polygon.centroid.x*first_cell.polygon.centroid.y
        #     ]],
        #     columns=self.conf.ShapelyStructureColumns
        # )
        first_cell_structure = first_cell._cell_to_structure_columns()
        print("first cell structure {}".format(first_cell_structure))
        first_cell_df = first_cell._cell_to_structure_df()
        print("first cell dataframe {}".format(first_cell_df))
        self.CellStorage = self.CellStorage.append(first_cell_df)
        print("Cell storage\n{}\nEnd cell storage".format(self.CellStorage))
        self.world.new_tectonic_plate(self.CellStorage)
        # raise Exception
        for x in range(default_size):
            self.subdivide()



    def add_cell(self, shp_cell: ShapelyCell):
        """
        Add a ShapelyCell to the ShapelyStructure
        :param shp_cell:
        :return:
        """
        self.CellStorage = self.CellStorage.append({
            'TectonicCell': shp_cell.world_cell,
            'ShapelyCell': shp_cell,
            'geometry': shp_cell._geom()
        })

    def subdivide(self):
        """
        Subdivides every cell of the GridStructure into two both horizontally and vertically
        (for a total of four new cells in the place of every one original cell)
        :return:
        """
        n = [x.subdivide() for x in self.CellStorage['ShapelyCell']]
        self.CellStorage = gpd.GeoDataFrame(columns=self.conf.ShapelyStructureColumns)
        self.world.clear_tectonic_plates()
        # print("After subdivide, n length {}".format(len(n)))
        for m1 in n:
            print("m1", len(m1), m1)
            m_as_df = gpd.GeoDataFrame(data=m1, columns=self.conf.ShapelyStructureColumns)
            print("m as df\n{}\nend m as df".format(m_as_df))
            self.world.new_tectonic_plate(m_as_df)
            for m in m1:
                # print("m",len(m),type(m),m)
                # print("World tectonic cells\n{}\nend world tectonic cells".format(self.world.tectonicPlatesDf))
                # raise Exception
                self.CellStorage = self.CellStorage.append(m, ignore_index=True)
                # print("Cell storage ShapelyCell column\n{}\nEnd Cell storage ShapelyCell column".format(self.CellStorage['ShapelyCell']))
                # print("Cell storage pos column\n{}\nEnd Cell storage pos column".format(
                #     self.CellStorage['pos']))
                # print("Cell storage age diff column\n{}\nEnd Cell storage age diff column".format(
                #     self.CellStorage['age_diff']))

    def update_cells(self,update_bounds: bool = True):
        print("Cell storage pre-update len {}, contents\n{}\nEnd cell storage pre-update".format(len(self.CellStorage),self.CellStorage))
        new_structure = gpd.GeoDataFrame(columns=self.conf.ShapelyStructureColumns)
        n = [x.update_structure(new_structure) for x in self.CellStorage['ShapelyCell']]
        # self.CellStorage = new_structure
        new_bounds = None
        for m in n:
            # print("m", type(m), m)
            new_structure = new_structure.append(m, ignore_index=True)
            # print("New structure with-duplicates len {}, contents\n{}\nEnd new structure with-duplicates".format(len(new_structure), new_structure))

            if len(m) != 1:
                raise Exception("Somehow, you got {} rows when updating the values for one row of ShapelyStructure!".format(len(m)))
            new_pos = m.iloc[0]['pos_point']
            # print("new_pos {} {}".format(type(new_pos),new_pos))
            new_shpcell = m.iloc[0]['ShapelyCell']
            # print("new_shpcell {} {} {}".format(type(new_shpcell), new_shpcell,new_shpcell.bounds))
            print("NEW AGE {}".format(m.iloc[0]['age_diff']))
            m_bounds = new_shpcell.bounds
            if update_bounds is False:
                pass
            elif new_bounds is None:
                new_bounds = list(m_bounds)
            else:
                for bound in range(max(len(new_bounds),len(m_bounds))):
                    new_bounds[bound] = max(new_bounds[bound],m_bounds[bound])
                    # print("bound {}, {}".format(new_bounds[bound],m_bounds[bound]))
                # print("new bounds {}".format(new_bounds))

                # raise Exception
            matching_rows = new_structure.loc[new_structure['pos_point'] == new_pos]
            # print("matching rows\n{}\nEnd matching rows".format(matching_rows))
            if len(matching_rows) > 1:
                new_matching_rows = matching_rows.loc[matching_rows['ShapelyCell'] != m.iloc[0]['ShapelyCell']]
                # print("new matching rows\n{}\nEnd new matching rows".format(new_matching_rows))
                new_structure.drop(matching_rows.index, inplace=True)
                updated_m = m.iloc[0]['ShapelyCell'].join_cells(new_matching_rows['ShapelyCell'])
                # updated_m = m.iloc[0]['ShapelyCell'].update_structure(new_structure)
                # print("Updated m\n{}\nend updated m".format(updated_m))
                new_structure = new_structure.append(updated_m, ignore_index=True)
                # new_structure = new_structure.append(m, ignore_index=True)

                # print("New structure NO duplicates len {}, contents\n{}\nEnd new structure NO duplicates".format(len(new_structure), new_structure))
                # raise Exception

            # print("Cell storage ShapelyCell column\n{}\nEnd Cell storage ShapelyCell column".format(
            #     self.CellStorage['ShapelyCell']))
            # print("Cell storage pos column\n{}\nEnd Cell storage pos column".format(
            #     self.CellStorage['pos']))
            # print("Cell storage age diff column\n{}\nEnd Cell storage age diff column".format(
            #     self.CellStorage['age_diff']))
        # print("New structure len {}, contents\n{}\nEnd new structure".format(len(new_structure), new_structure))
        # raise Exception
        self.CellStorage = new_structure

        # print("After subdivide, n length {},contents\n{}\nEnd cell storage after update".format(len(n),n))
        # raise Exception

    def move_cell_in_structure(self,column_title,cell_value,move_x,move_y):
        try:
            iter(column_title)
            matching_rows = self.CellStorage.loc[self.CellStorage[column_title].isin(cell_value)]
        except TypeError:
            matching_rows = self.CellStorage.loc[self.CellStorage[column_title] == cell_value]
        print("Before drop\n{}\nend before drop".format(self.CellStorage))
        self.CellStorage.drop(matching_rows.index, inplace=True)
        print("After drop\n{}\nend after drop".format(self.CellStorage))
        # self.CellStorage.drop(self.CellStorage[column_title] == cell_value)
        print("Matching rows\n{}\nend matching rows".format(matching_rows))
        # lambda_results  = self.CellStorage.assign(Percentage = lambda x: (x['Total_Marks'] /500 * 100))
        lambda_results = matching_rows.apply(lambda x: self.move_single_cell(x,move_x,move_y,change_velocity=True), axis=1)
        print("lambda results\n{}\nend lambda results".format(lambda_results))
        # raise Exception

    def move_single_cell(self,cell_row,move_x,move_y, change_velocity: bool = False, allow_update: bool=True):
        old_move_x = copy.deepcopy(move_x)
        old_move_y = copy.deepcopy(move_y)
        if self.wrap is True:

            print("Wrapping movement ({},{})".format(move_x,move_y))
            print("Cell perimeter {}".format(cell_row['ShapelyCell'].exterior))
            cell_perimeter = cell_row['ShapelyCell'].exterior
            cell_coords = list(cell_perimeter.coords)
            cell_bounds = [cell_coords[0][0],cell_coords[0][1],cell_coords[0][0],cell_coords[0][1]]
            print("Cell perimeter {}\ncoords {}\nbounds {}".format(cell_perimeter,cell_coords,cell_bounds))
            for pt in cell_coords:
                print("cell coords point {}".format(pt))
                cell_bounds[0] = min(cell_bounds[0],pt[0])
                cell_bounds[1] = min(cell_bounds[1], pt[1])
                cell_bounds[2] = max(cell_bounds[2], pt[0])
                cell_bounds[3] = max(cell_bounds[3], pt[1])
            print("cell bounds {}".format(cell_bounds))
            wrapped_pos = self._wrap_position((move_x, move_y),cell_bounds)
            move_x = wrapped_pos[0]
            move_y = wrapped_pos[1]
        print("Movement ({},{})".format(move_x, move_y))
        print("Original structure\n{}\n{}\nend original structure".format(self,self.CellStorage['geometry']))
        print("cell row to be moved type: {}, individual: {}".format(type(cell_row),cell_row))
        shapely_cell = cell_row['ShapelyCell']
        print("move single cell cell: {}, move_x: {}, move_y: {}".format(shapely_cell,move_x,move_y))
        if self.wrap is True and (move_x != old_move_x or move_y != old_move_y):
            velocity_offset = [0,0]
            if move_x > old_move_x:
                velocity_offset[0] = self.bounds[2]-self.bounds[0]
            elif move_x < old_move_x:
                velocity_offset[0] = self.bounds[0]-self.bounds[2]
            if move_y > old_move_y:
                velocity_offset[1] = self.bounds[3] - self.bounds[1]
            elif move_y < old_move_y:
                velocity_offset[1] = self.bounds[1] - self.bounds[3]
            moved_cell = shapely_cell.move(move_x,move_y,change_velocity=change_velocity,velocity_offset=velocity_offset)
            # raise Exception
        else:
            moved_cell = shapely_cell.move(move_x,move_y,change_velocity=change_velocity)
        if allow_update is True:
            # moved_cell = shapely_cell.move(move_x, move_y, change_velocity=change_velocity)
            print("Moved cell\n{}\nend moved cell".format(moved_cell))
            print("Path {} of moved_cell.last_skew_path\n{}\nEnd path of moved_cell.last_skew_path".format(type(moved_cell.last_skew_path),moved_cell.last_skew_path))
            if type(moved_cell.last_skew_path) is not GeometryCollection and len(moved_cell.last_skew_path) > 0:
                plt_geom(moved_cell.last_skew_path, title="moved_cell.last_skew_path")
            skew_path = unary_union(moved_cell.last_skew_path['geometry'])
            print("Path {} of skew_path\n{}\nEnd path of skew_path".format(type(skew_path), skew_path))






            if type(skew_path) is not GeometryCollection:
                plt_geom(skew_path, title="skew_path")
                # raise Exception
                print("Moved cell polygon\n{}\nend moved cell polygon".format(moved_cell.polygon))
                # =
                overlapping_rows = self.find_overlap(skew_path)
                #     print("overlapping rows\n{}\nend overlapping rows".format(overlapping_rows))
                #     plt_geoms(overlapping_rows)
                    # raise Exception
                # overlapping_rows = self.find_overlap(cell_row)
                print("{} overlapping results \n{}\nEnd overlapping results".format(len(overlapping_rows), overlapping_rows['overlap']))
                fully_overlapping_rows = overlapping_rows.loc[overlapping_rows['overlap'] < 2]
                print("{} Fully overlapping results \n{}\nEnd fully overlapping results".format(len(fully_overlapping_rows), fully_overlapping_rows['overlap']))
                line_adjacent_overlapping_rows = overlapping_rows.loc[overlapping_rows['overlap'] == 3.2]
                print("{} Adjacent results \n{}\nEnd adjacent results".format(len(line_adjacent_overlapping_rows), line_adjacent_overlapping_rows['overlap']))
                pt_adjacent_overlapping_rows = overlapping_rows.loc[overlapping_rows['overlap'] == 3.2]
                print("{} Diagonally adjacent results \n{}\nEnd diagonally adjacent results".format(len(pt_adjacent_overlapping_rows), pt_adjacent_overlapping_rows['overlap']))
                prob1 = overlapping_rows['overlap'] >= 2
                prob2 = overlapping_rows['overlap'] < 3
                # print("prob1\n{}\nend prob1".format(prob1))
                # print("prob2\n{}\nend prob2".format(prob2))
                prob3 = prob1 & prob2
                # print("prob3\n{}\nend prob3".format(prob3))
                problematic_rows = overlapping_rows.loc[prob3]

                print("{} Problem (incomplete intersection) results (col 'overlap') \n{}\nEnd problem results".format(len(problematic_rows), problematic_rows['overlap']))
                print("{} Problem (incomplete intersection) results \n{}\nEnd problem results".format(len(problematic_rows), problematic_rows))
                semi_overlap = problematic_rows.drop(['overlap'], axis=1)
                print("{} semi overlap \n{}\nEnd semi overlap".format(
                    len(semi_overlap), semi_overlap))

                # self.add_color()

                # semi_overlap.append(cell_row)
                # print("{} semi overlap \n{}\nEnd semi overlap".format(
                #     len(semi_overlap), semi_overlap))

                # plt_geoms(moved_cell.last_skew_path)
                # TODO: Use last_skew_path to determine which cells should be absorbed
                plt_geoms([moved_cell.polygon,skew_path,fully_overlapping_rows], title="Full overlap", fill=True)
                plt_geoms([moved_cell.polygon,skew_path, line_adjacent_overlapping_rows, pt_adjacent_overlapping_rows,], title="Line overlap", fill=True)
                plt_geoms([moved_cell.polygon,skew_path, semi_overlap], title="Semi overlap", fill=True)
                plt_geoms([moved_cell.polygon,skew_path,fully_overlapping_rows,line_adjacent_overlapping_rows,pt_adjacent_overlapping_rows,semi_overlap],title="All overlaps",fill=True)
                # raise Exception

                cells_at_position = fully_overlapping_rows
                print("Cells at position\n{}\nend cells at position".format(cells_at_position))
                if len(cells_at_position) > 0:
                    print("OLD STACK SIZE {}".format(moved_cell.world_cell.stack_size))
                    new_stack_size = moved_cell.world_cell.stack_size + len(cells_at_position)
                    print("NEW STACK SIZE {}".format(new_stack_size))
                    new_world_cell = copy.deepcopy(moved_cell.world_cell)
                    new_world_cell.stack_size = new_stack_size
                    print("New world cell {}".format(new_world_cell))
                    moved_cell.world_cell = new_world_cell

                    self.CellStorage.drop(cells_at_position.index, inplace=True)
                self.CellStorage = moved_cell.update_structure(self.CellStorage)
                print("Updated structure\n{}\n{}\nend updated structure".format(self, self.CellStorage['geometry']))
                overlapping_rows = self.find_overlap(skew_path)
                fully_overlapping_rows = overlapping_rows.loc[overlapping_rows['overlap'] < 2]
                print("{} Fully overlapping results \n{}\nEnd fully overlapping results".format(
                    len(fully_overlapping_rows), fully_overlapping_rows['overlap']))
                plt_geoms([moved_cell.polygon, skew_path, fully_overlapping_rows], title="Full overlap AFTER", fill=True)

                cells_at_position = semi_overlap
                print("Cells at position\n{}\nend cells at position".format(cells_at_position))
                if len(cells_at_position) > 0:
                    print("OLD STACK SIZE {}".format(moved_cell.world_cell.stack_size))
                    new_stack_size = moved_cell.world_cell.stack_size + len(cells_at_position)
                    print("NEW STACK SIZE {}".format(new_stack_size))
                    new_world_cell = copy.deepcopy(moved_cell.world_cell)
                    new_world_cell.stack_size = new_stack_size
                    print("New world cell {}".format(new_world_cell))
                    moved_cell.world_cell = new_world_cell

                    self.CellStorage.drop(cells_at_position.index, inplace=True)
                self.CellStorage = moved_cell.update_structure(self.CellStorage)
                print("Updated structure\n{}\n{}\nend updated structure".format(self, self.CellStorage['geometry']))
                overlapping_rows = self.find_overlap(skew_path)
                fully_overlapping_rows = overlapping_rows.loc[overlapping_rows['overlap'] < 2]
                print("{} Fully overlapping results \n{}\nEnd fully overlapping results".format(
                    len(fully_overlapping_rows), fully_overlapping_rows['overlap']))

        # raise Exception









        # if allow_update is True:
        #     cells_at_position = self.CellStorage.loc[self.CellStorage['pos_point'] == moved_cell.centroid]
        #     print("Cells at position\n{}\nend cells at position".format(cells_at_position))
        #     if len(cells_at_position) > 0:
        #         print("OLD STACK SIZE {}".format(moved_cell.world_cell.stack_size))
        #         new_stack_size = moved_cell.world_cell.stack_size + len(cells_at_position)
        #         print("NEW STACK SIZE {}".format(new_stack_size))
        #         new_world_cell = copy.deepcopy(moved_cell.world_cell)
        #         new_world_cell.stack_size = new_stack_size
        #         print("New world cell {}".format(new_world_cell))
        #         moved_cell.world_cell = new_world_cell
        #
        #         self.CellStorage.drop(cells_at_position.index, inplace=True)
        #     self.CellStorage = moved_cell.update_structure(self.CellStorage)
        #     print("Updated structure\n{}\n{}\nend updated structure".format(self,self.CellStorage['geometry']))
        #     # cells_at_position = self.CellStorage.loc[self.CellStorage['pos_point'] == moved_cell.centroid]
        #     # print("Cells at position\n{}\nend cells at position".format(cells_at_position))
        #     # if len(cells_at_position) > 1:
        #     #     moved_cell.world_cell.stack_size += len(cells_at_position)-1
        #     #     print("STACK SIZE {}".format(moved_cell.world_cell.stack_size))
        #     #     raise Exception

        return moved_cell

    def add_color(self,row,color):
        return color

    def _wrap_position(self,pos,cell_bounds):
        x = pos[0]
        y = pos[1]
        print("Wrapping movement ({},{})".format(x, y))
        print("cell bounds {}".format(cell_bounds))
        print("Bounds {}".format(self.bounds))
        old_x = x
        old_y = y
        bound_x_width = (self.bounds[2] - self.bounds[0])
        bound_y_width = (self.bounds[3] - self.bounds[1])
        print("Figure bounds x width {}, y width {}".format(bound_x_width,bound_y_width))
        mod_x = x % bound_x_width
        mod_y = y % bound_y_width
        print("Modded x {}, y {}".format(mod_x,mod_y))
        x = mod_x + self.bounds[0]
        y = mod_y + self.bounds[1]
        print("Wrapped x {}, y {}".format(x, y))
        if cell_bounds is not None:
            cell_bound_x_width = cell_bounds[2]-cell_bounds[0]
            half_cell_bound_x_width = cell_bound_x_width/2
            cell_bound_y_width = cell_bounds[3]-cell_bounds[1]
            half_cell_bound_y_width = cell_bound_y_width / 2
            print("Cell bounds x width {}, y width {}".format(half_cell_bound_x_width, half_cell_bound_y_width))
            # TODO: THESE AREN'T CORRECT. NEED TO FIX.
            # min_x = x - (cell_bounds[2]-cell_bounds[0])/2
            # max_x = x + (cell_bounds[2]-cell_bounds[0])/2
            # min_y = y - (cell_bounds[3]-cell_bounds[1])/2
            # max_y = y + (cell_bounds[3]-cell_bounds[1])/2
            # print("Position with bounds ({} {} {} {})".format(min_x,min_y,max_x,max_y))
            min_x = x + cell_bounds[0]
            max_x = cell_bounds[2] + x
            min_y = y + cell_bounds[1]
            max_y = cell_bounds[3] + y
            print("Position with bounds ({} {} {} {})".format(min_x, min_y, max_x, max_y))
            if max_x > self.bounds[2]:
                if min_x < self.bounds[0]:
                    raise Exception("Cell is larger than bounds, cannot be placed")
                else:
                    x -= bound_x_width
                    print("Had to reposition x right to {}".format(x))
            if min_x < self.bounds[0]:
                x += bound_x_width
                print("Had to reposition x left to {}".format(x))
            if max_y > self.bounds[3]:
                if min_y < self.bounds[1]:
                    raise Exception("Cell is larger than bounds, cannot be placed")
                else:
                    y -= bound_y_width
                    print("Had to reposition y right to {}".format(y))
            if min_y < self.bounds[1]:
                y += bound_y_width
                print("Had to reposition y left to {}".format(y))
            min_x = x + cell_bounds[0]
            max_x = cell_bounds[2] + x
            min_y = y + cell_bounds[1]
            max_y = cell_bounds[3] + y
            print("Repositioned with bounds ({} {} {} {})".format(min_x, min_y, max_x, max_y))
            # raise Exception
        print("New move ({}, {})".format(x, y))
        if old_x != x or old_y != y:
            print("Old move ({}, {})".format(x, y))
        return (x,y)

    def random_cell(self):
        print("Cell storage is len {}".format(len(self.CellStorage)))
        randint = random.randint(0,len(self.CellStorage)-1)
        print("Random number {}".format(randint))
        randomrow = self.CellStorage.iloc[randint]
        # randomcell = randomrow['ShapelyCell']
        # print("Random cell {}".format(randomcell))
        # raise Exception
        return randomrow

    def move_random_cell(self, fill_gap: bool = True, force_movement: bool = True, scale_movement: bool = True):
        cellrow = self.random_cell()
        shpcell = cellrow['ShapelyCell']
        x_movement = random.randint(-1,1)
        y_movement = random.randint(-1,1)
        if force_movement is True:
            while x_movement == 0 and y_movement ==0:
                x_movement = random.randint(-1, 1)
                y_movement = random.randint(-1, 1)
        if scale_movement is True:
            x_movement *= shpcell.x_size
            y_movement *= shpcell.y_size
        print("shpcell {} bounds {} age".format(shpcell, shpcell.bounds,shpcell.creation_age))
        print("x {}, y {}".format(shpcell.x_size, shpcell.y_size))
        if fill_gap is True:
            old_cell = cellrow['ShapelyCell']
            old_perim = old_cell.exterior
            print("old cell age {}".format(old_cell.creation_age))
            fill_cell = ShapelyCell(conf=old_cell.conf,shell=old_perim)
            fill_cell.world_cell.setWorld(old_cell.world_cell.world)
            print("fill cell age {}".format(fill_cell.creation_age))
            print("Old perimeter {}".format(old_perim))
            fill_row = fill_cell._cell_to_structure_df()
            print("fill row {}, vel {}, pos {}, age {}".format(fill_row, fill_cell.velocity, fill_cell.centroid, fill_cell.world_cell.age))
            print("age diff {}".format(fill_row['age_diff']))
            print("World age {}".format(self.conf.world.age))
            self.CellStorage = self.CellStorage.append(fill_row, ignore_index=True)
            # raise Exception
        self.move_single_cell(cellrow,x_movement,y_movement,change_velocity=True)

    def move_cell(self, cell, velocity, fill_gap: bool = True, scale_movement: bool = False, allow_update: bool = True):
        print("Input cell {}, velocity {}".format(cell, velocity))
        print("input cell world cell {}".format(cell.world_cell.world))
        cellrow = self.CellStorage.loc[self.CellStorage['ShapelyCell']==cell]
        print("moving cell of cell row type {}: {}".format(type(cellrow),cellrow))
        if len(cellrow) is 0:
            return
            # blank_series = pd.Series(data=[False]*len(self.conf.ShapelyStructureColumns),index=self.conf.ShapelyStructureColumns)
            # print("blank series\n{}\nEnd blank series".format(blank_series))
            # return blank_series
        cellrow = cellrow.iloc[0]
        print("moving cell of cell row type {}: {}".format(type(cellrow),cellrow))
        shpcell = cellrow['ShapelyCell']
        print("velocity {}, coords".format(velocity,velocity.coords))
        x_movement = velocity.coords[1][0]-velocity.coords[0][0]
        y_movement = velocity.coords[1][1]-velocity.coords[0][1]
        print("x movement {}".format(x_movement))
        print("y movement {}".format(y_movement))
        # raise Exception
        if scale_movement is True:
            x_movement *= shpcell.x_size
            y_movement *= shpcell.y_size
        print("shpcell {} bounds {} age; world cell {}".format(shpcell, shpcell.bounds, shpcell.creation_age, shpcell.world_cell))
        print("x size {}, y size {}".format(shpcell.x_size, shpcell.y_size))
        fill_row=None
        # raise Exception
        if fill_gap is True:
            old_cell = cellrow['ShapelyCell']
            print("old cell {} world {}".format(old_cell, old_cell.world_cell.world))
            old_perim = old_cell.exterior
            print("old cell age {}".format(old_cell.creation_age))
            fill_cell = ShapelyCell(conf=old_cell.conf, shell=old_perim)
            fill_cell.world_cell.setWorld(old_cell.world_cell.world)
            print("fill cell age {}".format(fill_cell.creation_age))
            print("fill cell world {}".format(fill_cell.world_cell.world))
            print("Old perimeter {}".format(old_perim))
            fill_row = fill_cell._cell_to_structure_df()
            print("fill row {}, vel {}, pos {}, age {}".format(fill_row, fill_cell.velocity, fill_cell.centroid,
                                                               fill_cell.world_cell.age))
            print("age diff {}".format(fill_row['age_diff']))
            print("World age {}".format(self.conf.world.age))
            self.CellStorage = self.CellStorage.append(fill_row, ignore_index=True)

        print("Moving single cell")
        self.move_single_cell(cellrow, x_movement, y_movement, change_velocity=True,allow_update=allow_update)
        print("fill row type {}\n{}\nEnd fill row".format(type(fill_row),fill_row))
        print("fill cell\n{}\nend fill cell".format(fill_row.iloc[0]['ShapelyCell'].polygon))
        # raise Exception
        return fill_row.iloc[0]



        # raise Exception

    def step_move(self):
        matching_rows = self.CellStorage.loc[self.CellStorage['speed'] > 0]
        print("Cells with a velocity")
        print(matching_rows)
        moved_cells = matching_rows.apply(lambda x: self.move_existing_velocity(x),axis=1)
        # if len(matching_rows) > 0:
            # raise Exception

    def move_existing_velocity(self, cellrow, fill_gap: bool = True):
        print("Moving with existing velocity cell {}".format(cellrow))
        existing_velocity = cellrow['ShapelyCell'].velocity
        move_x = (existing_velocity.coords[1][0]-existing_velocity.coords[0][0])
        move_y = (existing_velocity.coords[1][1]-existing_velocity.coords[0][1])
        print("Move x {}, y {}".format(move_x,move_y))
        # raise Exception

        if fill_gap is True:
            old_cell = cellrow['ShapelyCell']
            old_perim = old_cell.exterior
            print("old cell age {}".format(old_cell.creation_age))
            fill_cell = ShapelyCell(conf=old_cell.conf,shell=old_perim)
            fill_cell.world_cell.setWorld(old_cell.world_cell.world)
            print("fill cell age {}".format(fill_cell.creation_age))
            print("Old perimeter {}".format(old_perim))
            fill_row = fill_cell._cell_to_structure_df()
            print("fill row {}, vel {}, pos {}, age {}".format(fill_row, fill_cell.velocity, fill_cell.centroid, fill_cell.world_cell.age))
            print("age diff {}".format(fill_row['age_diff']))
            print("World age {}".format(self.conf.world.age))
            self.CellStorage = self.CellStorage.append(fill_row, ignore_index=True)
            # raise Exception


        return self.move_single_cell(cellrow, move_x, move_y, change_velocity=False)
        # raise Exception

    def find_neighbors(self,cell):
        print("given cellrow {}".format(cell))
        # TODO: Convert to gpd
        lambda_results = pd.DataFrame(self.CellStorage)
        print("copy lambda results \n{}\nEnd copy lambda results".format(lambda_results))
        lambda_results['overlap'] = self.CellStorage.apply(lambda x: self.overlap_type(x, cell), axis=1)
        print("lambda results \n{}\nEnd lambda results".format(lambda_results))
        print("lambda results overlap \n{}\nEnd lambda results overlap".format(lambda_results['overlap']))
        overlapping_rows = lambda_results.loc[lambda_results['overlap'] != 0]
        print("{} overlapping results \n{}\nEnd overlapping results".format(len(overlapping_rows),overlapping_rows))
        # print("{} overlapping results \n{}\nEnd overlapping results".format(len(overlapping_rows),overlapping_rows['overlap']))
        neighboring_results = overlapping_rows.loc[overlapping_rows['overlap'] == 3.1]
            # overlapping_rows['overlap'] == 3.1
        print("{} neighboring results \n{}\nEnd neighboring results".format(len(neighboring_results),
                                                                            neighboring_results))
        # neighboring_rows = self.CellStorage.loc[neighboring_results]
        # print("{} neighboring results \n{}\nEnd neighboring results".format(len(neighboring_rows),
        #                                                                     neighboring_rows))
        return neighboring_results
        # overlapping_rows =

    def find_overlap(self, cellrow):
        print("given cellrow {}".format(cellrow))
        # TODO: Convert to gpd
        lambda_results = gpd.GeoDataFrame(self.CellStorage)
        lambda_results['overlap'] = self.CellStorage.apply(lambda x: self.overlap_type(x, cellrow), axis=1)
        # print("lambda results \n{}\nEnd lambda results".format(lambda_results))
        overlapping_rows = lambda_results.loc[lambda_results['overlap'] != 0]
        # print("{} overlapping results \n{}\nEnd overlapping results".format(len(overlapping_rows),overlapping_rows['overlap']))
        return overlapping_rows

    def overlap_type(self,c1_row, c2_row):
        print("overlap type for c1 {}, c2 {}".format(type(c1_row),type(c2_row)))
        if type(c1_row) is not Polygon:
            if type(c1_row) is not ShapelyCell:
                c1 = c1_row['ShapelyCell'].polygon
        else:
            c1 = c1_row
        if type(c2_row) is not Polygon:
            if type(c2_row) is not ShapelyCell:
                c2 = c2_row['ShapelyCell'].polygon
        else:
            c2 = c2_row
        if c1.almost_equals(c2):
            print("{} and {} fully overlap".format(c1,c2))
            return 1.3
        if c1.contains(c2):
            print("{} within {} or reverse".format(c1, c2))
            return 1.121
        if c2.contains(c1):
            print("{} within {}".format(c2,c1))
            return 1.212
        if c1.touches(c2):
            # print("{} touches {}".format(c1,c2))
            print("Touches along {}".format(c1.intersection(c2)))
            print("Type of intersection {}".format(type(c1.intersection(c2))))
            if type(c1.intersection(c2)) is LineString:
                return 3.1
            else:
                return 3.2
        if c1.intersects(c2):
            # print("{} intersects {}".format(c1,c2))
            print("Intersection size {}".format(c1.intersection(c2).area))
            print("Polygon areas {}, {}".format(c1.area,c2.area))
            return 2.3
        return 0


    def __str__(self):
        return str(self.CellStorage)
