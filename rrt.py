import math
import random
from collections import defaultdict
import make_graph
import cv2
import matplotlib.pyplot as plt
import numpy as np


def convNpToArray(vector):
    return tuple(np.ndarray.tolist(vector))


def checkCollisions(point1, point2):
    vector = point2 - point1
    a = 0.01
    while True:
        temp_point = point1 + a * vector
        if round(temp_point[0]) == 50 and round(temp_point[1]) < 60:
            return True
        a += 0.01
        if a > 1:
            return False


def findDistance(point1, point2):
    return np.linalg.norm(point1 - point2)

plt.figure("map")
graph = make_graph.Make_graph()

starting_point = np.array([10, 10])
ending_point = (90, 10)

points = [starting_point]
points_dict = defaultdict()
points_dict[convNpToArray(starting_point)] = 0
step_distance = 6
current_point = np.array(starting_point)

graph.add_node((50, 60), (50, 0))

while (len(points) < 200):
    search_radius = 2
    random_point = np.array([random.randint(0, 100), random.randint(0, 100)])
    min_dist = 10000
    for point in points:
        temp_dist = findDistance(random_point, point)
        if min_dist > temp_dist:
            min_dist = temp_dist
            current_point = point

    scaling_factor = step_distance / findDistance(random_point, current_point)
    new_point = current_point + (scaling_factor * (random_point - current_point))


    for point in points:
        if findDistance(point, new_point) < step_distance * search_radius and points_dict[convNpToArray(point)] + findDistance(point, new_point)< points_dict[
            convNpToArray(current_point)] + findDistance(current_point, new_point):
            if not checkCollisions(point, current_point):
                current_point = point

    if checkCollisions(new_point, current_point):
        continue

    points_dict[convNpToArray(new_point)] = findDistance(new_point, current_point) + points_dict[convNpToArray(current_point)]
    points.append(new_point)
    #graph.add_node(current_point, new_point)
    graph.add_node(new_point, current_point)
    """
    for point in points:
        if convNpToArray(point) not in graph.return_graph().values() and convNpToArray(point) not in graph.return_graph().keys():
            print(point, graph.return_graph())
        else:
            print("in")
            pass
    """

    for point in points:
        if findDistance(point, new_point) < step_distance * search_radius and points_dict[convNpToArray(point)] > points_dict[
            convNpToArray(new_point)] + findDistance(new_point, point):
            if not checkCollisions(point, new_point):
                points_dict[convNpToArray(point)] = findDistance(new_point, point) + points_dict[convNpToArray(new_point)]
                #graph.delete_node(point)
                #graph.add_node(new_point, point)
                graph.delete_node(new_point)
                graph.add_node(point, new_point)
    graph.draw_graph(points_dict)


plt.figure("test")
