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

points_in_graph = [starting_point]
distances_from_start = defaultdict()
distances_from_start[convNpToArray(starting_point)] = 0

step_distance = 6
closest_point = np.array(starting_point)

graph.add_node((50, 60), (50, 0)) #obstacles

while (len(points_in_graph) < 200):
    search_radius = 2
    random_point = np.array([random.randint(0, 100), random.randint(0, 100)])
    min_dist = 10000
    for point in points_in_graph:
        temp_dist = findDistance(random_point, point)
        if min_dist > temp_dist:
            min_dist = temp_dist
            closest_point = point

    scaling_factor = step_distance / findDistance(random_point, closest_point)
    new_point = closest_point + (scaling_factor * (random_point - closest_point))

    if checkCollisions(closest_point, new_point):
        continue
    for point in points_in_graph:
        if findDistance(point, new_point) < step_distance * search_radius and distances_from_start[convNpToArray(point)] + findDistance(point, new_point)< distances_from_start[
            convNpToArray(closest_point)] :
            if not checkCollisions(point, new_point):
                closest_point = point


    distances_from_start[convNpToArray(new_point)] = findDistance(new_point, closest_point) + distances_from_start[convNpToArray(closest_point)]
    points_in_graph.append(new_point)
    graph.add_node(closest_point, new_point)


    for point in points_in_graph:
        if findDistance(point, new_point) < step_distance * search_radius and distances_from_start[convNpToArray(point)] > distances_from_start[
            convNpToArray(new_point)] + findDistance(new_point, point):
            if not checkCollisions(point, new_point):
                distances_from_start[convNpToArray(point)] = findDistance(new_point, point) + distances_from_start[convNpToArray(new_point)]
                graph.delete_node(point)
                print(point)
                graph.add_node(new_point, closest_point)
    graph.draw_graph(distances_from_start)


plt.figure("test")