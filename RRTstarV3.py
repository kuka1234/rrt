from collections import defaultdict

import random
import networkx as nx
import numpy as np
import node as node_library
import imageToGraph
import scipy.stats as stats
import time
from matplotlib import pyplot as plt


img = imageToGraph.ready_image()
map_range_x = img.shape[1]
map_range_y = img.shape[0]


start_point = (124,464)
end_point = (1032,49)
radius = 70
search_factor = 60  # need to optimise
new_distance = 20
available_points = imageToGraph.get_all_points(img)

start_node = node_library.Node(start_point, "start", root=True)

def findDistance(point_1, point_2): # finds distance between 2 points
    return np.linalg.norm(np.asarray(point_1) - np.asarray(point_2))

def scaleDown(point_1, point_2): # scales down the line connecting 2 points, sf = distance of final line.
    x = np.asarray(point_1)+ ((np.asarray(point_2)- np.asarray(point_1))*(new_distance/np.linalg.norm((np.asarray(point_2)- np.asarray(point_1)))))
    return (x[0], x[1])


def checkForCollisons(point_1, point_2): # returns True if there is an obstacle between 2 points
    vector =  np.asarray(point_2) -  np.asarray(point_1)
    a = 0.1
    while True:
        temp_point = point_1 + a * vector
        if imageToGraph.get_obstacle(temp_point[0], temp_point[1]):
            return True
        a += 0.1
        if a > 1:
            return False

def flatten(container): # used to convert a nested list to a flattened list
    for i in container:
        if isinstance(i, (list)):
            for j in flatten(i):
                yield j
        else:
            yield i


def visualise():
    plt.imshow(img, cmap='gray')
    for i in range(1000):
        point = get_random_point()
        plt.scatter(point[0], point[1], s = 0.6, c='black')
    plt.scatter(end_point[0], end_point[1], s= radius)
    plt.show()

random.seed(200211)  #200231, 200211

def get_random_point(): # finds random point depending on normal distribution
    random_point = random.choice(available_points)
    return random_point

def find_closest_node(random_point, start_node): # creates random point and finds closest node to that point
    closest_node = None
    for i in start_node.get_list_of_nodes():
        if ((closest_node == None) or ((findDistance(i.name, random_point) < findDistance(closest_node.name, random_point)))):
            closest_node = i

    if checkForCollisons(scaleDown(closest_node.name, random_point), closest_node.name):
        closest_node = None

    return closest_node

def check_new_parent_node(new_point, start_node):
    for i in start_node.get_list_of_nodes():
        temp_dist = findDistance(i.name, new_point.name)
        if temp_dist< search_factor and temp_dist + i.getDistance() < new_point.getDistance() and not checkForCollisons(i.name, new_point.name):
            new_point.changeParent(i)

def check_for_child_node(new_point, start_node):
    # checks if any nodes close to the new node can be connected to the new node to form a short path. New node -> node
    for i in start_node.get_list_of_nodes():
        temp_dist = findDistance(i.name, new_point.name)
        if temp_dist< search_factor and temp_dist + new_point.getDistance() < i.getDistance() and not checkForCollisons(
                i.name, new_point.name):
            i.changeParent(new_point)

def check_for_shorter_paths():
    for i in start_node.get_list_of_nodes():
        for j in start_node.get_list_of_nodes():
            if findDistance(i.name, j.name)< search_factor and findDistance(i.name, j.name) + j.getDistance() < i.getDistance() and not checkForCollisons(i.name, j.name):
                i.changeParent(j)

def get_min_dist():
    min_dist = 10000
    for i in start_node.get_list_of_nodes():
        if findDistance(i.name, end_point) < min(70,min_dist):
            min_dist = i.getDistance()
    return min_dist

def main_loop():
    random_point = get_random_point()
    closest_node = find_closest_node(random_point, start_node)
    if closest_node == None:
        return

    new_point = node_library.Node(scaleDown(closest_node.name, random_point), closest_node)
    check_new_parent_node(new_point, start_node) #??
    check_for_child_node(new_point, start_node) #??
    #check_for_shorter_paths()


G = nx.Graph() # graph of nodes

def draw_network():
    temp_dict = {}
    path_to_start = []
    G.clear()

    min_dist = 10000
    for i in start_node.get_list_of_nodes():
        temp_dict[i.name] = i.name
        if i.is_root == False:
            G.add_edge(i.name, i.parent.name)
            if findDistance(i.name, end_point) < min(70,min_dist): #7
                path_to_start = list(flatten(i.getPath()))

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
            colors.append('blue')

    nx.draw_networkx(G, pos = temp_dict, with_labels= False, node_size=200/map_range_x, edge_color = colors)



    plt.imshow(img, cmap='gray')
    plt.pause(0.000001)
    #plt.clf()


#visualise()
start_time = time.time()
iterations = 5000 #5000
for i in range(iterations):

    if (i % 1000) == 0:
        check_for_shorter_paths()

    if (i % 500) == 0:
        print(str(round(i/iterations * 100)) + "%" + "---" + str(round(time.time() - start_time)) + "s")
        draw_network()
        plt.show()
        plt.clf()
    main_loop()


draw_network()
print("done")

plt.show()
