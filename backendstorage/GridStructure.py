from backendstorage.ArrayStructure import ArrayStructure

class GridStructure(ArrayStructure):
    def __init__(self, width=2, height=2, **kwargs):
        super(GridStructure, self).__init__(**kwargs)
        self.cellShape = 'rectangle'
        self.cellClassName = 'GridCell'
        self.cellClassFile = 'backendstorage.GridCell'
        self.cellClass = self.conf.class_for_name(module_name=self.cellClassFile, class_name=self.cellClassName)
        self.width = width
        self.height = height
        self._ArrayStorage = [[None] * self.width] * self.height

        # print("thing gridstructure {}".format(self[0]))
        counter = 0
        cells = []
        for selem in self:
            # from backendstorage.GridCell import GridCell
            # selem = counter
            cell = self.cellClass()
            cells.append(cell)
            selem = cell
            # selem = self.cellClass()
            print("selem {} {}".format(type(selem),selem))
            counter += 1
        print(cells)
        print("SELF",self)

        for selem in self:
            print("new selem",selem)




