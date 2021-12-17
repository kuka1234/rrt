import math
from collections import defaultdict
import make_graph
import cv2
import matplotlib.pyplot as plt
import numpy as np

img = cv2.imread("C:/Users/shree/Downloads/Inkedbasement_LI.jpg", cv2.IMREAD_GRAYSCALE)  # stores grayscale image in img

#plt.figure("orignal_image")
#plt.imshow(img, cmap='gray')


def scale_down(img, scale_percent):
    img = cv2.resize(img, (int(img.shape[1] * scale_percent / 100), int(img.shape[0] * scale_percent / 100)),
                     interpolation=cv2.INTER_AREA)
    return img


def define_borders(img, color_of_border):
    mask = cv2.inRange(img, np.array([color_of_border - 5]), np.array([color_of_border + 5]))
    img[mask > 0] = 0
    return img


def dilate_edge(img, amount):
    kernel = np.ones((amount, amount), np.uint8)
    img = cv2.erode(img, kernel, iterations=1)
    return img


# post processing to make edges well defined.
img = define_borders(img, 205)
img = scale_down(img, 5)
img = dilate_edge(img, 1)

# used to visualise the distance map
plt.figure("post_processing")
plt.imshow(img, cmap='gray')


def make_graph_from_dict(my_dict):  # func not needed
    local_graph = make_graph.Make_graph()
    for key in my_dict:
        local_graph.add_node(key, my_dict[key])
    local_graph.draw_graph({})


def convert_img_into_dict(img, color_of_path):  # converts image in np.array form into a dictonary.
    def addtoDict(current, adjacent, local_dict):
        if (img[adjacent[0], adjacent[1]]) in range(color_of_path - 100, color_of_path + 100):
            local_dict[(current[1], current[0])].append((adjacent[1], adjacent[0]))
        return local_dict

    local_dict = defaultdict(list)
    rows, cols = img.shape
    for i in range(0, rows):
        for j in range(0, cols):
            if (i > 0):
                local_dict = addtoDict([i, j], [i - 1, j], local_dict)
            if (j > 0):
                local_dict = addtoDict([i, j], [i, j - 1], local_dict)
            if (i < rows - 1):
                local_dict = addtoDict([i, j], [i + 1, j], local_dict)
            if (j < cols - 1):
                local_dict = addtoDict([i, j], [i, j + 1], local_dict)
    return local_dict
plt.figure("grid")
graph_of_image = make_graph.Make_graph()
dictionary = convert_img_into_dict(img, 200)
graph_of_image.set_graph(dictionary)
graph_of_image.draw_graph({})
#plt.show()
# Uses BFS to make heuristic.
# params for make_heuristic #
que = []
visited = set()
heur_dict = {}
distance = 0


# params for make_heuristic #
def make_heuristic(dictionary, distance, counter):
    """
    while que:
        vertex = que.pop(0)
        for neighbour in dictionary[vertex]:
            if neighbour not in visited:
                if counter == 0:
                    counter = neighbour
                que.append(neighbour)
                visited.add(neighbour)
                heur_dict[neighbour] = distance

        if counter == vertex:
            counter = 0
            distance += 1

        make_heuristic(dictionary, distance, counter)
    return heur_dict
    """


starting_point = (60, 15)
ending_point = (51, 15)

que.append(ending_point)  # because distance would be lowest at end point for heuristic
#distances_dict = make_heuristic(dictionary, 0, 0)

"""
# used to visualise the distance map
plt.figure("heuristic")
distance_map = make_graph.Make_graph()
distance_map.set_graph(dictionary)
distance_map.draw_graph(distances_dict)
print("Heuristic made")
"""
# A* #

# sets up params for A*
unvisited = []
for node in dictionary:
    unvisited.append(node)
distances = {}
for node in dictionary:
    distances[node] = 10000000000000
distances[starting_point] = 0
parents = {starting_point: [starting_point]}


def a_star(cur):
    if cur == ending_point:
        return
    unvisited.remove(cur)
    for neighbour in dictionary[cur]:
        if neighbour not in unvisited:
            continue
        if distances[neighbour] > distances[cur] + 1:
            distances[neighbour] = distances[cur] + 1
            temp_list = parents[cur].copy()
            temp_list.append(cur)
            parents[neighbour] = temp_list
    next_node, shortest_distance = None, 1000
    for node in unvisited:
        try:
            #if distances[node] + distances_dict[node] * heuristic_factor < shortest_distance:
            #    next_node, shortest_distance = node, distances[node] + distances_dict[node] * heuristic_factor
            if math.dist(node, ending_point) + distances[node] < shortest_distance:
                next_node, shortest_distance = node, distances[node] + math.dist(node, ending_point)

        except:
            pass

    a_star(next_node)


heuristic_factor = 5  # how much should the heuristic matter, extremely high value can cause an error.
a_star(starting_point)
print("A-star algo done")
# used to visualise all points visited by a_star.
plt.figure("points visted by A*")
astar_graph = make_graph.Make_graph()
for key in parents.keys():
    astar_graph.add_node(key, parents[key][-1])
astar_graph.draw_graph({})


def dict_list_to_dict(my_list):  # converts values of last node in dictionary to "linked list"
    path = {}  # will store path from end to
    path_list = my_list[list(my_list.keys())[-1]]  # gets path connected to node in list form
    for i in range(len(path_list) - 1):
        path[path_list[i]] = path_list[i + 1]
    return path


path = dict_list_to_dict(parents)

# used to visulaise final path.
plt.figure("final path")
final_path_graph = make_graph.Make_graph()
final_path_graph.set_graph(path)
final_path_graph.draw_graph({})

plt.show()
