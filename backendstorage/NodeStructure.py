from backendstorage.GeneralStructure import *
from backendstorage.Node import *

class NodeStructure(GeneralStructure):
    def __init__(self, **kwargs):
        self.startNode = Node()
        self.endNode = self.startNode
        self.id = 0
        super(NodeStructure, self).__init__(**kwargs)

    def addNeigbor(self,originNode,destinationNode):
        originNode.neighbors.add(destinationNode)
        destinationNode.neighbors.add(originNode)
        if originNode.id == -1:
            originNode.id = self.id
            self.id += 1
        if destinationNode.id == -1:
            destinationNode.id = self.id
            self.id += 1

    def update_neighbors(self):
        for node in self:
            nbrs = node.neighbors
            for nbr in nbrs:
                if node not in nbr.neighbors:
                    nbr.neighbors.add(node)

    def print_contents(self):
        print("PRINTING CONTENTS OF A NODE STRUCTURE")
        for node in self:
            strAdditions = '{}'
            if node == self.endNode:
                strAdditions = "(end) " + strAdditions
            if node == self.startNode:
                strAdditions = "(start) " + strAdditions
            print("\t"+strAdditions.format(node))
            print("\t\t" + node.neighbor_string())
        print("DONE PRINTING NODE STRUCTURE")




    def __iter__(self):
        itr = NodeIterator(nodestruct=self)
        # print("iterator:",itr, "current:", itr._current, "visited:",itr._visited, "missing:", itr._missing)
        return itr

class NodeIterator(GeneralIterator):
    def __init__(self, nodestruct, **kwargs):
        self._nodestruct = nodestruct
        self._current = self._nodestruct.startNode
        self._visited = set()
        self._missing = set()
        super(NodeIterator, self).__init__(**kwargs)

    def __next__(self):
        neighbors = self._current.neighbors
        if self._current not in self._visited:
            self._missing.add(self._current)

        for nbr in neighbors:
            if nbr in self._visited:
                continue
            self._missing.add(nbr)

        while len(self._missing) > 0:
            # print("MISSING",self._missing)
            next = self._missing.pop()
            if next.id == -1:
                next.id = self._nodestruct.id
                self._nodestruct.id += 1
            if next not in self._visited:
                self._visited.add(next)
                return next


        raise StopIteration



