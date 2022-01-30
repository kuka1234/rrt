import numpy as np
"""
a = np.array([1.0, 3.5, -6.3])
b = np.array([4.5, 1.6,  1.2])

dist = np.linalg.norm(a-b)
"""
class Node:
    all_nodes = []

    def __init__(self,name, parent, root = False):
        self.name = name
        self.parent = parent
        self.is_root = root
        Node.all_nodes.append(self)

    def changeParent(self, new_parent):
        self.parent = new_parent

    def getDistance(self):
        if self.is_root == False:
            return np.linalg.norm(np.asarray(self.name)-np.asarray(self.parent.name)) + self.parent.getDistance()
        else:
            return 0

    def getPath(self):
        if self.is_root == False:
            #return str(str(self.name) + str(self.parent.path()))
            return [self.name, self.parent.getPath()]
        else:
            return "start"

    @classmethod
    def get_list_of_nodes(cls):
        return cls.all_nodes

