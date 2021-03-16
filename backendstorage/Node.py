class Node:
    def __init__(self, id=-1):
        self.neighbors = set()
        self.id = id

    def __str__(self):
        return "Node (id {})  with {} neighbors".format(self.id,len(self.neighbors))

    def neighbor_string(self):
        nbrs = []
        nbr_str = ''
        for nbr in self.neighbors:
            nbrs.append(nbr)
            nbr_str += str(nbr) + ' '
        return 'Node with {} neighbors: ({})'.format(len(self.neighbors), nbr_str)