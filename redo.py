from collections import defaultdict

import random
import networkx as nx
import numpy as np
import node as node_library
import imageToGraph
import scipy.stats as stats
from matplotlib import pyplot as plt

img = imageToGraph.ready_image()
map_range_x = img.shape[1]
map_range_y = img.shape[0]

#node0 = node_library.Node((img.shape[0],img.shape[1]), "start", root=True)
start_node = node_library.Node((200, 600), "start", root=True)
end_point = (1200,230)
plt.figure(1)

def findDistance(point_1, point_2):
    return np.linalg.norm(np.asarray(point_1) - np.asarray(point_2))

def scaleDown(point_1, point_2, sf = 40):
    #x = np.asarray(point_1)+ ((np.asarray(point_1)-np.asarray(point_2))*sf/np.linalg.norm(np.asarray(point_1)-np.asarray(point_2)))
    x = np.asarray(point_1)+ ((np.asarray(point_2)- np.asarray(point_1))*(sf/np.linalg.norm((np.asarray(point_2)- np.asarray(point_1)))))
    return (x[0], x[1])

def checkForCollisons(point_1, point_2):
    vector =  np.asarray(point_2) -  np.asarray(point_1)
    a = 0.01
    while True:
        temp_point = point_1 + a * vector
        if imageToGraph.get_obstacle(temp_point[0], temp_point[1]):
            return True
        a += 0.01
        if a > 1:
            return False
def flatten(container):
    for i in container:
        if isinstance(i, (list)):
            for j in flatten(i):
                yield j
        else:
            yield i

random.seed(200211)  #200231, 200211
def main_loop():
    search_factor = 60 #need to optimise
    #random_point = (random.randint(0, map_range_x), random.randint(0,map_range_y))

    random_point = round(stats.skewnorm(2 if end_point[0] < map_range_x/2 else -2, end_point[0], max(map_range_x-end_point[0], end_point[0])/2).rvs(1)[0]), round(stats.skewnorm(2 if end_point[1] < map_range_y/2 else -2, end_point[1], max(map_range_y-end_point[1], end_point[1])/2).rvs(1)[0])
    closest_node = start_node
    temp_var = False
    #creates random point and finds closest node to that point
    for i in start_node.get_list_of_nodes():
        if findDistance(i.name, random_point)< findDistance(closest_node.name, random_point) and not checkForCollisons(scaleDown(i.name, random_point), i.name):
            for j in start_node.get_list_of_nodes():
                if findDistance(j.name, scaleDown(i.name, random_point))< 20:
                    break
            else:
                temp_var = True
                closest_node = i

    if temp_var == False and len(start_node.get_list_of_nodes())> 1:
        print("increase")
        return

    #checks for duplicates; can happen later on
    for i in start_node.get_list_of_nodes():
        if i.name == scaleDown(closest_node.name, random_point):
            return "duplicated point" + "see if statement"

    # creates new point at a specific distance from the closest node
    if not checkForCollisons(scaleDown(closest_node.name, random_point), closest_node.name):
        new_point = node_library.Node(scaleDown(closest_node.name, random_point), closest_node)
    else:
        return

    #looks for shorter paths to the start by searching area around the new node, if there is one the new node will connect to a new parent. Node -> new node
    for i in start_node.get_list_of_nodes():
        if findDistance(i.name, new_point.name)< search_factor and findDistance(i.name, new_point.name) + i.getDistance() < new_point.getDistance() and not checkForCollisons(i.name, new_point.name):
            new_point.changeParent(i)

    #checks if any nodes close to the new node can be connected to the new node to form a short path. New node -> node
    for i in start_node.get_list_of_nodes():
        if findDistance(i.name, new_point.name)< search_factor and findDistance(i.name, new_point.name) + new_point.getDistance() < i.getDistance() and not checkForCollisons(i.name, new_point.name):
            i.changeParent(new_point)

    for i in start_node.get_list_of_nodes():
        for j in start_node.get_list_of_nodes():
            if findDistance(i.name, j.name)< search_factor and findDistance(i.name, j.name) + j.getDistance() < i.getDistance() and not checkForCollisons(i.name, j.name):
                i.changeParent(j)

G = nx.Graph() # graph of nodes

def draw_network():
    temp_dict = {}
    path_to_start = []
    G.clear()
    plt.clf()

    min_dist = 10000
    for i in start_node.get_list_of_nodes():
        if i.is_root == False:
            G.add_edge(i.name, i.parent.name)
            if findDistance(i.name, end_point) < min(70,min_dist): #7
                path_to_start = list(flatten(i.getPath()))


    for i in G:
        temp_dict[i] = i

    values = []

    for i in G.nodes:
        for j in start_node.get_list_of_nodes():
            if i == j.name:
                if j.name in path_to_start:
                    values.append(0)
                else:
                    values.append(j.getDistance())

    colors = []
    for u, v in G.edges():
        for i in range(len(path_to_start)):
            try:
                if (u == path_to_start[i] and v == path_to_start[i+1]) or (u == path_to_start[i+1] and v == path_to_start[i]):
                    colors.append('red')
                    break
            except:
                pass
        else:
            colors.append('black')

    nx.draw_networkx(G, pos = temp_dict, with_labels= False, node_size=200/map_range_x, node_color= values, cmap=plt.get_cmap('viridis'), edge_color = colors)


    img = imageToGraph.ready_image()
    plt.imshow(img, cmap='gray')
    plt.pause(0.0001)
    #plt.show()

"""
for i in range(1000):
    plt.scatter(round(stats.skewnorm(2 if end_point[0] < map_range_x/2 else -2, end_point[0], max(map_range_x-end_point[0], end_point[0])/2.3).rvs(1)[0]), round(stats.skewnorm(2 if end_point[1] < map_range_y/2 else -2, end_point[1], max(map_range_y-end_point[1], end_point[1])/2.3).rvs(1)[0]),s =1, c='black')
plt.imshow(imageToGraph.ready_image())
plt.show()
"""

iterations = 500 #5000
for i in range(iterations):
    if i % 100 == 0:
        print(str(round(i/iterations * 100)) + "%")
    main_loop()
    draw_network()

draw_network()
print("done")

plt.show()

##need to add##
# way of optimising sf and search factor
# change variance depending on failed attempts
# make new file which is optimised
