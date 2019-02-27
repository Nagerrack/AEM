import time

import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.distance import euclidean

file_path = r'objects.data'


def result_scores(result_list):
    return min(result_list), max(result_list), sum(result_list) / len(result_list)


def measure_execution_time(func, parameters):
    start = time.time()
    func(*parameters)
    stop = time.time()
    time_elapsed = stop - start
    # print(time_elapsed)
    return time_elapsed


def distance_matrix(x, y):
    matrix = np.zeros((len(x), len(y)))
    for i, x_coords in enumerate(x):
        for j, y_coords in enumerate(y):
            matrix[i, j] = euclidean(x_coords, y_coords)
    return matrix


def plot_points(point_list):
    x, y = zip(*point_list)
    plt.scatter(x[:len(x) // 2], y[:len(y) // 2], c='r')
    plt.scatter(x[len(x) // 2:], y[len(x) // 2:], c='b')

    # plt.scatter(x, y)
    plt.show()


def prims_iteration(tree, nodes_left, dist_matrix):
    distances = {}
    for i in tree:
        for j in nodes_left:
            distances[(i, j)] = dist_matrix[i, j]
    print(distances)
    print(min(distances, key=distances.get))


def mst_sum(tree):
    return 1


with open(file_path) as data_file:
    points = []
    for line in data_file:
        points.append([int(number) for number in line.split()])

# print(points)
# print(len(points))
# print(distance_matrix(points, points))

plot_points(points)
prims_iteration([0, 1, 2], [3, 4, 5, 6, 7, 8], distance_matrix(points, points))
