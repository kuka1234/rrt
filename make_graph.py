from collections import defaultdict

import networkx as nx
import numpy
from matplotlib import pyplot as plt


class Make_graph:
    def __init__(self):
        self.graph = defaultdict(list)
    def add_node(self, vertex, neighbours):
        if type(neighbours) == tuple:
            #self.graph[tuple(reversed(vertex))].append(tuple(reversed(neighbours)))
            self.graph[vertex].append(neighbours)
        elif type(neighbours) == list:
            for i in neighbours:
                self.graph[tuple(reversed(vertex))].append(tuple(reversed(i)))
        elif type(neighbours).__module__ == numpy.__name__ :
                #self.graph[tuple(map(tuple, vertex))].append(tuple(map(tuple, neighbours)))
                #self.graph[tuple(numpy.ndarray.tolist(vertex))].append(tuple(numpy.ndarray.tolist(neighbours)))
                self.graph[tuple(numpy.ndarray.tolist(vertex))].append(tuple(numpy.ndarray.tolist(neighbours)))
        else:
            raise Exception("neighbours is of wrong type")
    def set_graph(self, user_graph):
        self.graph = user_graph

    def delete_node(self, vertex):
        try:
            x = list(self.graph.values()).index(tuple(numpy.ndarray.tolist(vertex)))
            print(self.graph.keys())
            #self.graph.pop(list(self.graph.keys())[x])
        except:
            #print(tuple(numpy.ndarray.tolist(vertex)))
            #print(self.graph)
            pass

        """
        try:
            x = list(self.graph.values()).index(tuple(numpy.ndarray.tolist(vertex)))
            self.graph.pop(list(self.graph.keys())[x])
            #self.graph.pop(list(self.graph.keys())[list(self.graph.values()).index(tuple(numpy.ndarray.tolist(vertex)))])
        except:
            print(self.graph)
            print(tuple(numpy.ndarray.tolist(vertex)))
            pass
        """
    def return_graph(self):
        return self.graph

    def draw_graph(self, distances):
        G = nx.Graph()
        temp_dict = defaultdict()
        for i in self.return_graph():
            neighbours =  self.return_graph()[i]
            if type(neighbours) == tuple:
                G.add_edge(i,neighbours)
            elif type(neighbours == list):
                for j in neighbours:
                    G.add_edge(i,j)
            else:
                raise Exception("Graph is not in correct data structure")

        for node in G:
            temp_dict[node] = node

        values = [distances.get(node, 1) for node in G.nodes()]
        nx.draw_networkx(G, pos = temp_dict, node_size=10, node_color= values, with_labels=False, cmap=plt.get_cmap('viridis'))


        ax = plt.gca()
        plt.xlim([0, 100])
        plt.ylim([0, 100])
        #ax.set_ylim(ax.get_ylim()[::-1])
        #plt.show()

        plt.pause(0.000000001)
