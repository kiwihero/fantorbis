from backendstorage.Cell import Cell
import copy
class GridCell(Cell):
    def __init__(self, parent=None, customkwargs=None, **kwargs):
        print("custom kwargs",customkwargs)
        print("gridcell kwargs",kwargs)
        super(GridCell, self).__init__(**kwargs)
        self.parent = parent
        self.ckwargs = customkwargs
        self.kwargs = kwargs
        if self.ckwargs is None:
            self.ckwargs = {}


        # if 'childClass' in self.ckwargs:
        if 'parent' in self.ckwargs and self.parent is None:
            self.parent = [self.ckwargs['parent']]

        if 'child' in self.ckwargs:
            self.children = [self.ckwargs['child']]
        elif 'childClass' in self.ckwargs:
            self.childClass = self.ckwargs['childClass']
            self.children = []
            child = self.childClass()
            self.children.append(child)
        else:
            self.childClass = None
            self.children = []
        if 'conf' in self.ckwargs:
            self.conf = self.ckwargs['conf']
            self.world = self.conf.world
            for child in self.children:
                self.world.tectonicCells.add(child)



    def __copy__(self):
        newCell = GridCell(parent=self.parent, **self.kwargs)
        newCell.conf = self.conf
        if self.childClass is not None:
            newCell.childClass = self.childClass
            newCell.children = [newCell.childClass()]
        newCell.world = self.conf.world
        for child in newCell.children:
            newCell.world.tectonicCells.add(child)
        return newCell

    def __deepcopy__(self, memodict={}):
        print("memodict",memodict)
        newCell = GridCell(parent=self.parent, customkwargs=self.ckwargs, **self.kwargs)
        newCell.conf = self.conf
        if self.childClass is not None:
            self.children.append(self.childClass())
        newCell.world = self.conf.world
        for child in newCell.children:
            newCell.world.tectonicCells.add(child)
        print("new cell",newCell)
        return newCell

    def __str__(self):
        return 'Object of type {} with parent {}, children {} (class {})'.format(type(self), type(self.parent), self.children, self.childClass)