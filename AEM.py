import random
import time

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from scipy.spatial.distance import euclidean


def load_points(file_path):
    with open(file_path) as data_file:
        return [[int(number) for number in line.split()] for line in data_file]


def result_scores(result_list):
    return min(result_list), max(result_list), sum(result_list) / len(result_list)


def measure_execution_time_and_result(func, parameters):
    start = time.time()
    result = func(*parameters)
    stop = time.time()
    time_elapsed = stop - start
    # print(time_elapsed)
    return result, time_elapsed


def experiment_measurements(func, parameters, dist_matrix, points):
    result_dict = {}
    for i in range(100):
        result, time_elapsed = measure_execution_time_and_result(func, parameters)
        result_dict[round(sum_all_groups(result, dist_matrix), 3)] = (result, time_elapsed)

    max_group, time_elapsed1 = result_dict[max(result_dict)]
    min_group, time_elapsed2 = result_dict[min(result_dict)]
    plot_groups(max_group, points, save=True, name='MaxFigure')
    plot_groups(min_group, points, save=True, name='MinFigure')

    print('Min:{0}, {3}s; Max:{1}, {4}s; Average:{2}, {5}s', *result_scores(result_dict.keys()),
          round(result_dict[min(result_dict)][1], 2), round(result_dict[max(result_dict)][1], 2),
          round(result_scores([result[1] for result in result_dict.values()][2]), 2))
    # print('Time:')
    # print('Min:{}, Max:{}, Average:{}', *result_scores([result[1] for result in result_dict.values()]))


def distance_matrix(x, y):
    matrix = np.zeros((len(x), len(y)))
    for i, x_coords in enumerate(x):
        for j, y_coords in enumerate(y):
            matrix[i, j] = euclidean(x_coords, y_coords)
    return matrix


def prims_iteration(tree, nodes_left, dist_matrix):
    distances = {}
    for i in tree:
        for j in nodes_left:
            distances[(i, j)] = dist_matrix[i, j]
    print(distances)
    print(min(distances, key=distances.get))


def append_mst(tree, point, dist_matrix):
    edge_dict = {(node, point): dist_matrix[node, point] for node in tree.nodes()}
    tree.add_edge(*min(edge_dict, key=edge_dict.get))


def mst_append_cost(tree, point, dist_matrix):
    return min({(node, point): dist_matrix[node, point] for node in tree.nodes()}.values())


def count_mst_length(tree, dist_matrix):
    return sum([dist_matrix[edge] for edge in tree.edges()])


def sum_all_groups(groups, dist_matrix):
    return sum([count_mst_length(groups, dist_matrix) for group in groups])


# the groups are represented as a list of 10 lists containing points
# after an initialisation each group contains a randomly chosen point
def init_groups(points, groups_number=10):
    groups = [nx.Graph() for _ in range(groups_number)]

    for i in range(groups_number):
        index = random.randint(0, len(points))
        groups[i].add_node(index)

    return groups


# finds n groups which have the smallest minimal spanning trees after adding a new point
def find_n_min_msts(point, groups, distances, n=3):
    groups_mst = []

    for i in range(len(groups)):
        # todo: insert actual function that counts the length of a minimal spanning tree (instead of 'count_mst_length')
        groups_mst.append([i, count_mst_length(groups[i] + point, distances)])

    return sorted(groups_mst, key=lambda l: l[1])[:n]


# for each point:
# 1. finds 3 groups with smallest mst (in a case when the point was added to the group)
# 2. adds the point to a randomly chosen group (to one of those 3)
def grasp(points, distances):
    groups = init_groups(points)

    '''
    for point in points:
        min_msts = find_n_min_msts(point, groups, distances)
        index = min_msts[random.randint(0, 3)][0]
        groups[index].append(point)
    '''

    return groups


def plot_groups(groups, points, save=False, name='figure'):
    colors = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#00FFFF',
              '#FF00FF', '#FF8C00', '#696969', '#7B68EE', '#7FFFD4', '#008080']

    color_dict = {i: colors[i] for i in range(len(colors))}

    for i in range(len(groups)):
        for j in groups[i].nodes():
            plt.scatter(*points[j], c=color_dict[i])
    plt.show()
    if save:
        plt.savefig(name + '.png')


def main():
    points = load_points(r'objects.data')
    distances = distance_matrix(points, points)

    # groups = grasp(points, distances)

    # plot_groups(groups)

    # print(count_mst_length([(1, 2), (2, 3), (5, 7), (2, 7), (7, 100)], distances))

    G = nx.Graph()
    H = nx.Graph()
    for i in range(0, 10):
        G.add_node(i)
    for i in range(10, 20):
        H.add_node(i)

    plot_groups([G, H], points)

    print(mst_append_cost(G, 100, distances))


main()
