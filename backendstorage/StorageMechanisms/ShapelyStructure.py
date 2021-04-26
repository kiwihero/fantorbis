import geopandas as gpd
import math
import copy

from backendstorage.StorageMechanisms.ArrayStructure import *
from backendstorage.Cells.ShapelyCell import ShapelyCell


class ShapelyStructure(ArrayStructure):
    """
    Not a real structure either, don't use this itself
    Structures that use arrays instead of pointers to hold information
    """
    def __init__(self, **kwargs):
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
        print("After subdivide, n length {}".format(len(n)))
        for m1 in n:
            print("m1", len(m1), m1)
            for m in m1:
                print("m",len(m),m)
                self.CellStorage = self.CellStorage.append(m, ignore_index=True)
                print("Cell storage ShapelyCell column\n{}\nEnd Cell storage ShapelyCell column".format(self.CellStorage['ShapelyCell']))
                print("Cell storage pos column\n{}\nEnd Cell storage pos column".format(
                    self.CellStorage['pos']))
                print("Cell storage age diff column\n{}\nEnd Cell storage age diff column".format(
                    self.CellStorage['age_diff']))

    def update_cells(self):
        print("Cell storage pre-update len {}, contents\n{}\nEnd cell storage pre-update".format(len(self.CellStorage),self.CellStorage))
        new_structure = gpd.GeoDataFrame(columns=self.conf.ShapelyStructureColumns)
        n = [x.update_structure(new_structure) for x in self.CellStorage['ShapelyCell']]
        # self.CellStorage = new_structure
        for m in n:
            print("m", type(m), m)
            new_structure = new_structure.append(m, ignore_index=True)
            print("New structure with-duplicates len {}, contents\n{}\nEnd new structure with-duplicates".format(len(new_structure), new_structure))

            if len(m) != 1:
                raise Exception("Somehow, you got {} rows when updating the values for one row of ShapelyStructure!".format(len(m)))
            new_pos = m.iloc[0]['pos_point']
            print("new_pos {} {}".format(type(new_pos),new_pos))
            matching_rows = new_structure.loc[new_structure['pos_point'] == new_pos]
            print("matching rows\n{}\nEnd matching rows".format(matching_rows))
            if len(matching_rows) > 1:
                new_matching_rows = matching_rows.loc[matching_rows['ShapelyCell'] != m.iloc[0]['ShapelyCell']]
                print("new matching rows\n{}\nEnd new matching rows".format(new_matching_rows))
                new_structure.drop(matching_rows.index, inplace=True)
                updated_m = m.iloc[0]['ShapelyCell'].join_cells(new_matching_rows['ShapelyCell'])
                # updated_m = m.iloc[0]['ShapelyCell'].update_structure(new_structure)
                print("Updated m\n{}\nend updated m".format(updated_m))
                new_structure = new_structure.append(updated_m, ignore_index=True)
                # new_structure = new_structure.append(m, ignore_index=True)

                print("New structure NO duplicates len {}, contents\n{}\nEnd new structure NO duplicates".format(len(new_structure), new_structure))
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
        lambda_results = matching_rows.apply(lambda x: self.move_single_cell(x,move_x,move_y), axis=1)
        print("lambda results\n{}\nend lambda results".format(lambda_results))
        # raise Exception

    def move_single_cell(self,cell_row,move_x,move_y):
        print("Original structure\n{}\n{}\nend original structure".format(self,self.CellStorage['geometry']))
        print("cell row to be moved type: {}, individual: {}".format(type(cell_row),cell_row))
        shapely_cell = cell_row['ShapelyCell']
        print("move single cell cell: {}, move_x: {}, move_y: {}".format(shapely_cell,move_x,move_y))
        moved_cell = shapely_cell.move(move_x,move_y)
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

    def __str__(self):
        return str(self.CellStorage)
