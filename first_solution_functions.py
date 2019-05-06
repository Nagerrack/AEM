import random
import networkx as nx
import numpy as np

from mst_helper import *


def is_distance_long_enough(point_id, indices, dist_matrix, min_distance):
    for id in indices:
        if dist_matrix[id, point_id] < min_distance:
            return False

    return True


# the groups are represented as a list of 20 graphs
# after an initialisation each group contains a point which is quite close to n other points (n = average group size)
def init_groups(points, dist_matrix, groups_number=20):
    groups = [nx.Graph() for _ in range(groups_number)]
    average_group_size = len(points) // groups_number
    min_dist = np.mean(dist_matrix) / 4
    min_distances = np.array([])
    indices = np.array([], dtype='int32')

    for i in range(len(points)):
        min_distances = np.append(min_distances, sum(np.sort(dist_matrix[i])[:average_group_size]))

    sorted_point_ids = min_distances.argsort()
    indices = np.append(indices, sorted_point_ids[0])

    for point_id in range(1, len(sorted_point_ids)):
        if not is_distance_long_enough(point_id, indices, dist_matrix, min_dist):
            continue

        indices = np.append(indices, point_id)
        if len(indices) >= groups_number:
            break

    for i in range(len(indices)):
        groups[i].add_node(indices[i])

    return groups, indices


# the groups are represented as a list of 10 lists containing points
# after an initialisation each group contains a randomly chosen point
def init_groups_random(points, groups_number=20):
    groups = [nx.Graph() for _ in range(groups_number)]
    indices = []

    for i in range(groups_number):
        index = random.randint(0, len(points) - 1)

        while index in indices:
            index = random.randint(0, len(points) - 1)

        indices.append(index)
        groups[i].add_node(index)

    return groups, indices


def get_init_sum_append_cost(node, group_nodes, dist_matrix):
    return sum([dist_matrix[node][i] for i in group_nodes])


# finds n groups which have the smallest minimal spanning trees after adding a new point
def find_n_min_msts(point_id, groups, distances, n=3):
    groups_mst = []

    for i in range(len(groups)):
        groups_mst.append([i, mst_append_cost(groups[i], point_id, distances)])

    return sorted(groups_mst, key=lambda l: l[1])[:n]


# finds 1 group which has the smallest average sum of distances between each pair
def find_min_average_distances_sum(point_id, groups, distances):
    min_group_id = 0
    min_append_cost = get_init_sum_append_cost(point_id, groups[0].nodes(), distances)

    for i in range(1, len(groups)):
        append_cost = get_init_sum_append_cost(point_id, groups[i].nodes(), distances)
        if min_append_cost > append_cost:
            min_append_cost = append_cost
            min_group_id = i

    return min_group_id


# for each point:
# 1. finds 3 groups with smallest mst (in a case when the point was added to the group)
# 2. adds the point to a randomly chosen group (to one of those 3)
def grasp(points, distances):
    groups, indices = init_groups_random(points)

    for i, point in enumerate(points):
        if i in indices:
            continue

        min_msts = find_n_min_msts(i, groups, distances)
        index = min_msts[0][0]
        groups[index].add_node(i)

    return groups


def grasp_fully_connected(points_left, groups, distances):
    for i in points_left:
        index = find_min_average_distances_sum(i, groups, distances)
        groups[index].add_node(i)

    return groups


# for each of n minimal MSTs finds the best appending of next points to group
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


def random_heuristic(points, dist_matrix, group_number=20):
    groups, indices = init_groups(points, dist_matrix)

    for i, point in enumerate(points):
        if i in indices:
            continue

        groups[random.randint(0, group_number - 1)].add_node(i)

    return groups
