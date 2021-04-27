import geopandas as gpd
import math
import copy
import random

from backendstorage.StorageMechanisms.ArrayStructure import *
from backendstorage.Cells.ShapelyCell import ShapelyCell


class ShapelyStructure(ArrayStructure):
    """
    Not a real structure either, don't use this itself
    Structures that use arrays instead of pointers to hold information
    """
    def __init__(self, wrap: bool = True, **kwargs):
        """
        This is an actual structure
        :param kwargs:
        """
        super(ShapelyStructure, self).__init__(**kwargs)
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
        # raise Exception



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
        # print("After subdivide, n length {}".format(len(n)))
        for m1 in n:
            # print("m1", len(m1), m1)
            for m in m1:
                # print("m",len(m),m)
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

    def move_single_cell(self,cell_row,move_x,move_y, change_velocity: bool = False):
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
        # moved_cell = shapely_cell.move(move_x, move_y, change_velocity=change_velocity)
        print("Moved cell\n{}\nend moved cell".format(moved_cell))
        print("Moved cell polygon\n{}\nend moved cell polygon".format(moved_cell.polygon))
        cells_at_position = self.CellStorage.loc[self.CellStorage['pos_point'] == moved_cell.centroid]
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
        print("Updated structure\n{}\n{}\nend updated structure".format(self,self.CellStorage['geometry']))
        # cells_at_position = self.CellStorage.loc[self.CellStorage['pos_point'] == moved_cell.centroid]
        # print("Cells at position\n{}\nend cells at position".format(cells_at_position))
        # if len(cells_at_position) > 1:
        #     moved_cell.world_cell.stack_size += len(cells_at_position)-1
        #     print("STACK SIZE {}".format(moved_cell.world_cell.stack_size))
        #     raise Exception
        return moved_cell

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
        print("Bound x width {}, y width {}".format(bound_x_width,bound_y_width))
        mod_x = x % bound_x_width
        mod_y = y % bound_y_width
        print("Modded x {}, y {}".format(mod_x,mod_y))
        x = mod_x + self.bounds[0]
        y = mod_y + self.bounds[1]
        print("Wrapped x {}, y {}".format(x, y))
        if cell_bounds is not None:
            min_x = x - (cell_bounds[2]-cell_bounds[0])/2
            max_x = x + (cell_bounds[2]-cell_bounds[0])/2
            min_y = y - (cell_bounds[3]-cell_bounds[1])/2
            max_y = y + (cell_bounds[3]-cell_bounds[1])/2
            print("Position with bounds ({} {} {} {})".format(min_x,min_y,max_x,max_y))
            min_x = cell_bounds[0] + x
            max_x = cell_bounds[2] + x
            min_y = cell_bounds[1] + y
            max_y = cell_bounds[3] + y
            print("Position with bounds ({} {} {} {})".format(min_x, min_y, max_x, max_y))
            if min_x < self.bounds[0]:
                if max_x > self.bounds[2]:
                    raise Exception("Cell is larger than bounds, cannot be placed")
                else:
                    x += (self.bounds[2] - self.bounds[0])
                    print("Had to reposition x right to {}".format(x))
            if max_x > self.bounds[2]:
                x -= (self.bounds[2] - self.bounds[0])
                print("Had to reposition x left to {}".format(x))
            if min_y < self.bounds[1]:
                if max_y > self.bounds[3]:
                    raise Exception("Cell is larger than bounds, cannot be placed")
                else:
                    y += (self.bounds[3] - self.bounds[1])
                    print("Had to reposition y right to {}".format(y))
            if max_y > self.bounds[3]:
                y -= (self.bounds[3] - self.bounds[1])
                print("Had to reposition y left to {}".format(y))
            # raise Exception
        print("New move ({}, {})".format(x, y))
        if old_x != x or old_y != y:
            print("Old move ({}, {})".format(x, y))
        return (x,y)

    def random_cell(self):
        print("Cell storage is len {}".format(len(self.CellStorage)))
        randint = random.randint(0,len(self.CellStorage)-1)
        print("Random number {}".format(randint))
        randomrow = self.CellStorage.loc[randint]
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
        print("shpcell {} bounds {}".format(shpcell, shpcell.bounds))
        print("x {}, y {}".format(shpcell.x_size, shpcell.y_size))
        if fill_gap is True:
            old_cell = cellrow['ShapelyCell']
            old_perim = old_cell.exterior
            fill_cell = ShapelyCell(conf=old_cell.conf, world_cell_args=old_cell.world_cell_args,shell=old_perim)
            print("Old perimeter {}".format(old_perim))
            fill_row = fill_cell._cell_to_structure_df()
            print("fill row {}, vel {}, pos {}, age {}".format(fill_row, fill_cell.velocity, fill_cell.centroid, fill_cell.world_cell.age))
            self.CellStorage = self.CellStorage.append(fill_row, ignore_index=True)
            # raise Exception
        self.move_single_cell(cellrow,x_movement,y_movement,change_velocity=True)

        # raise Exception

    def __str__(self):
        return str(self.CellStorage)
