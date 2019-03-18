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
    return round(min(result_list), 4), round(max(result_list), 4), round(sum(result_list) / len(result_list), 4)


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

    time_list = [result[1] for result in result_dict.values()]

    print('Min:{0}, {3}s; Max:{1}, {4}s; Average:{2}, {5}s'.format(
        *result_scores(result_dict.keys()),
        round(result_dict[min(result_dict)][1], 4),
        round(result_dict[max(result_dict)][1], 4),
        round(result_scores(time_list)[2], 4)
    ))
    # print('Time:')
    # print('Min:{}, Max:{}, Average:{}', *result_scores([result[1] for result in result_dict.values()]))


def distance_matrix(x, y):
    matrix = np.zeros((len(x), len(y)))
    for i, x_coords in enumerate(x):
        for j, y_coords in enumerate(y):
            matrix[i, j] = euclidean(x_coords, y_coords)
    return matrix


# append a point to a tree so that it remains being a MST
def append_mst(tree, point, dist_matrix):
    edge_dict = {(node, point): dist_matrix[node, point] for node in tree.nodes()}
    tree.add_edge(*min(edge_dict, key=edge_dict.get))


# count the cost of appending a chosen tree with a given point
def mst_append_cost(tree, point, dist_matrix):
    return min({(node, point): dist_matrix[node, point] for node in tree.nodes()}.values())


# count length of a MST
def count_mst_length(tree, dist_matrix):
    return sum([dist_matrix[edge] for edge in tree.edges()])


def sum_all_groups(groups, dist_matrix):
    return sum([count_mst_length(group, dist_matrix) for group in groups])


# the groups are represented as a list of 10 graphs
# after an initialisation each group contains a randomly chosen point
def init_groups(points, groups_number=10):
    groups = [nx.Graph() for _ in range(groups_number)]
    indices = []

    for i in range(groups_number):
        index = random.randint(0, len(points) - 1)

        while index in indices:
            index = random.randint(0, len(points) - 1)

        indices.append(index)
        groups[i].add_node(index)

    return groups, indices


# finds n groups which have the smallest minimal spanning trees after adding a new point
def find_n_min_msts(point_id, groups, distances, n=3):
    groups_mst = []

    for i in range(len(groups)):
        groups_mst.append([i, mst_append_cost(groups[i], point_id, distances)])

    return sorted(groups_mst, key=lambda l: l[1])[:n]


# for each point:
# 1. finds 3 groups with smallest mst (in a case when the point was added to the group)
# 2. adds the point to a randomly chosen group (to one of those 3)
def grasp(points, distances):
    groups, indices = init_groups(points)

    for i, point in enumerate(points):
        if i in indices:
            continue

        min_msts = find_n_min_msts(i, groups, distances)
        index = min_msts[random.randint(0, 2)][0]
        append_mst(groups[index], i, distances)

    return groups


# append a sequence of MSTs with a sequence of points
def append_sequence(groups, sequence, dist_matrix):
    for group, point in sequence:
        append_mst(groups[group], point, dist_matrix)


# for each of n minimal MSTs finds the best appending of a next points to group
# and returns dictionary with a key of sum cost of adding both points
def sum_regret(i, groups, min_msts, distances):
    cost_dict = {}
    for mst in min_msts:
        cost_sum = 0
        sequence = []
        group_index, cost = mst
        sequence.append((group_index, i))
        cost_sum += cost
        append_mst(groups[group_index], i, distances)
        next_group_index, next_cost = find_n_min_msts(i + 1, groups, distances, n=10)[0]
        sequence.append((next_group_index, i + 1))
        cost_sum += next_cost
        cost_dict[cost_sum] = sequence
        groups[group_index].remove_node(i)
    return cost_dict


# for each point:
# 1. finds 3 groups with smallest mst (in a case when the point was added to the group)
# 2. for each of these groups: finds the group with the smallest mst for a next point
# 3. chooses the sequence of appending MSTs with a smallest cost of appending both points
def regret(points, distances):
    groups, indices = init_groups(points)

    for i in range(len(points)):
        if i in indices:
            continue
        if i + 1 < len(points):
            min_msts = find_n_min_msts(i, groups, distances)
            cost_dict = sum_regret(i, groups, min_msts, distances)
            append_sequence(groups, cost_dict[min(cost_dict)], distances)

        else:
            min_msts = find_n_min_msts(i, groups, distances, n=1)
            index = min_msts[0][0]
            append_mst(groups[index], i, distances)

    return groups


def plot_groups(groups, points, save=False, name='figure'):
    colors = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#00FFFF',
              '#FF00FF', '#FF8C00', '#696969', '#7B68EE', '#7FFFD4', '#008080']

    color_dict = {i: colors[i] for i in range(len(colors))}

    for i in range(len(groups)):
        for j in groups[i].nodes():
            plt.scatter(*points[j], c=color_dict[i])

    if save:
        plt.savefig(name + '.png')
        plt.show()
    else:
        plt.show()


def main():
    points = load_points(r'objects.data')
    distances = distance_matrix(points, points)

    # experiment_measurements(grasp, [points, distances], distances, points)

    experiment_measurements(regret, [points, distances], distances, points)


main()
