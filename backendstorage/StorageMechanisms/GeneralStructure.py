from backendstorage.CustomExceptions import *
# # All of the structures inherit this
# # Declares some methods expected, default to returning an error when those are called and not implemented in inherited
class GeneralStructure:
    """
    This is NOT an actual structure, do not create instances of this
    """
    def __init__(self, conf=None, **kwargs):
        self.cellShape = None
        self.conf = conf
        # self._ArrayStorage = None
#         self.cellClassName = 'GridCell'
#         self.cellClassFile = 'backendstorage.GridCell'
#         if self.conf is not None:
#             self.cellClass = self.conf.class_for_name(module_name=self.cellClassFile, class_name=self.cellClassName)
#         else:
#             raise DoesNotExistError("self.conf")
#
    # def print_contents(self):
        """
        Iterate through the contents of the structure, printing them
        :return:
        """
        # raise DoesNotExistError("ArrayStorage")
#
#
    # def __iter__(self):
    #     raise DoesNotExistError("ArrayStorage")
#
#
#     def __str__(self):
#         return 'Data structure of some sort'.format()
#
#     def swap_cells(self, cell1, cell2):
#         tmp = cell1.pos
#         self.move_cell(cell1,cell2.pos)
#         self.move_cell(cell2, tmp)
#
#     def move_cell(self, cell, **kwargs):
#         raise StructureNotImplementedError("move_cell")
#
#     def add_cell(self, cell):
#         raise StructureNotImplementedError("move_cell")
#
#     def remove_cell(self, cell):
#         raise StructureNotImplementedError("move_cell")
#
#     def subdivide(self):
#         raise StructureNotImplementedError("subdivide")
#
#     def subdivide_rows(self):
#         raise StructureNotImplementedError("subdivide_rows")
#
#     def subdivide_cols(self):
#         raise StructureNotImplementedError("subdivide_cols")
#
class GeneralIterator:
    def __next__(self):
        raise StructureNotImplementedError("Iteration")
