import random
import networkx as nx
import numpy as np


def sum_pair_distances(group_nodes, dist_matrix):
    group_sum = 0

    for i in range(len(group_nodes)):
        group_sum += sum([dist_matrix[group_nodes[i], group_nodes[j]] for j in range(i + 1, len(group_nodes))])

    return group_sum


def average_sum_all_groups(groups, dist_matrix):
    distance_sums = []

    for group in groups:
        distance_sums.append(sum_pair_distances(group.nodes(), dist_matrix))

    return np.mean(distance_sums)


def average_pair_distances(group_nodes, dist_matrix):
    group_distances = np.array([])

    for node_i in group_nodes:
        group_distances = np.append(group_distances,
                                    [dist_matrix[node_i, node_j] for node_j in group_nodes if node_i > node_j])

    return np.mean(group_distances)


def sum_all_groups_fully_connected(groups, dist_matrix):
    sums = 0
    edges = 0
    for group in groups:
        group_nodes = group.nodes()
        nodes_count = len(group_nodes)
        sums += sum_pair_distances(group_nodes, dist_matrix)
        edges += (nodes_count * (nodes_count - 1)) / 2

    return sums / edges
