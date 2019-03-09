import time
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.distance import euclidean
import random

def load_points(file_path):
    with open(file_path) as data_file:
        return [[int(number) for number in line.split()] for line in data_file]


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
    plt.scatter(x, y, c='b')

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


def init_groups(points, groups_number=10):
    groups = []

    for i in range(groups_number):
        index = random.randint(0, len(points))
        groups.append(points[index])
        del points[index]

    return points, groups


def grasp(points, distances):
    points, groups = init_groups(points)


def main():
    points = load_points(r'objects.data')
    distances = distance_matrix(points, points)

    grasp(points, distances)

    plot_points(points)
    # prims_iteration([0, 1, 2], [3, 4, 5, 6, 7, 8], distance_matrix(points, points))

main()
