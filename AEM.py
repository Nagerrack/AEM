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


def count_mst_length(tree):
    pass


def mst_sum(tree):
    return 1

# the groups are represented as a list of 10 lists containing points
# after an initialisation each group contains a randomly chosen point
def init_groups(points, groups_number=10):
    groups = []

    for i in range(groups_number):
        index = random.randint(0, len(points))
        groups.append([points[index]])
        del points[index]

    return points, groups

# finds n groups which have the smallest minimal spanning trees after adding a new point
def find_n_min_msts(point, groups, distances, n=3):
    groups_mst = []

    for i in range(len(groups)):
        # todo: insert actual function that counts the length of a minimal spanning tree (instead of "count_mst_length")
        groups_mst.append([i, count_mst_length(groups[i] + point, distances)])

    return sorted(groups_mst,key=lambda l:l[1])[:n]

# for each point:
# 1. finds 3 groups with smallest mst (in a case when the point was added to the group)
# 2. adds the point to a randomly chosen group (to one of those 3)
def grasp(points, distances):
    points, groups = init_groups(points)

    '''
    for point in points:
        min_msts = find_n_min_msts(point, groups, distances)
        index = min_msts[random.randint(0, 3)][0]
        groups[index].append(point)
    '''

    return groups


def plot_groups(groups):
    colors = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#00FFFF', '#FF00FF', '#FF8C00', '#696969', '#7B68EE', '#7FFFD4', '#008080']

    for i in range(len(groups)):
        x, y = zip(*groups[i])
        plt.scatter(x, y, c=colors[i])

    plt.show()


def main():
    points = load_points(r'objects.data')
    distances = distance_matrix(points, points)

    groups = grasp(points, distances)

    plot_groups(groups)

    # plot_points(points)
    # prims_iteration([0, 1, 2], [3, 4, 5, 6, 7, 8], distance_matrix(points, points))

main()
