import random

import networkx as nx
import numpy as np
from scipy.spatial.distance import euclidean

from measurements import experiment_measurements


def load_points(file_path):
    with open(file_path) as data_file:
        return [[int(number) for number in line.split()] for line in data_file]


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


def sum_all_groups_mst(groups, dist_matrix):
    return sum([count_mst_length(group, dist_matrix) for group in groups])


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

    for i in range(len(group_nodes)):
        group_distances = np.append(group_distances, [dist_matrix[group_nodes[i], group_nodes[j]] for j in range(i + 1, len(group_nodes))])

    return np.mean(group_distances)


def sum_all_groups_fully_connected(groups, dist_matrix):
    return sum([average_pair_distances(group.nodes(), dist_matrix) for group in groups])


def is_distance_long_enough(point_id, indices, dist_matrix, min_distance):
    for id in indices:
        if dist_matrix[id, point_id] < min_distance:
            return False

    return True


# the groups are represented as a list of 10 graphs
# after an initialisation each group contains a point which is quite close to n other points (n = average group size)
def init_groups(points, dist_matrix, groups_number=10):
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
        if is_distance_long_enough(point_id, indices, dist_matrix, min_dist) == False:
            continue

        indices = np.append(indices, point_id)
        if len(indices) >= 10:
            break

    for i in range(len(indices)):
        groups[i].add_node(indices[i])

    return groups, indices


# finds n groups which have the smallest minimal spanning trees after adding a new point
def find_n_min_msts(point_id, groups, distances, n=3):
    groups_mst = []

    for i in range(len(groups)):
        groups_mst.append([i, mst_append_cost(groups[i], point_id, distances)])

    return sorted(groups_mst, key=lambda l: l[1])[:n]


def get_init_sum_append_cost(node, group_nodes, dist_matrix):
    return sum([dist_matrix[node, i] for i in group_nodes])

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
    groups, indices = init_groups(points, distances)

    for i, point in enumerate(points):
        if i in indices:
            continue

        index = find_min_average_distances_sum(i, groups, distances)
        groups[index].add_node(i)

    return groups


# append a sequence of MSTs with a sequence of points
def append_sequence(groups, sequence, dist_matrix):
    for group, point in sequence:
        append_mst(groups[group], point, dist_matrix)


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


# TODO
def local_search_greedy(groups, dist_matrix):
    return groups


def get_best_node_move(current_group_id, groups, node, dist_matrix):
    group_nodes = groups[current_group_id].nodes()
    current_average_dist = np.mean(np.array([dist_matrix[node, i] for i in group_nodes]))

    best_move = {'node': node, 'from': current_group_id, 'to': -1, 'profit': 0}

    for i, group in enumerate(groups):
        if i == current_group_id:
            continue

        group_nodes = group.nodes()
        average_dist = np.mean(np.array([dist_matrix[node, i] for i in group_nodes]))

        if (current_average_dist - average_dist) > best_move['profit']:
            best_move['to'] = i
            best_move['profit'] = current_average_dist - average_dist

    return best_move


def get_best_general_move(groups, dist_matrix):
    best_move = {'node': -1, 'from': -1, 'to': -1, 'profit': -1}

    for i, group in enumerate(groups):
        group_nodes = group.nodes()
        for node in group_nodes:
            move = get_best_node_move(i, groups, node, dist_matrix)

            if move['profit'] > best_move['profit']:
                best_move = move

    return best_move


def local_search_steep(groups, dist_matrix):
    best_move = {'node': -1, 'from': -1, 'to': -1, 'profit': 1}

    while best_move['profit'] > 0:
        best_move = get_best_general_move(groups, dist_matrix)
        if best_move['profit'] > 0:
            groups[best_move['from']].remove_node(best_move['node'])
            groups[best_move['to']].add_node(best_move['node'])

    return groups


def main():
    points = load_points(r'data/objects20_06.data')
    distances = distance_matrix(points, points)
    # experiment_measurements(grasp, [points, distances], sum_all_groups_fully_connected, distances, points, plot_suffix='_grasp')

    # experiment_measurements(regret, [points, distances], sum_all_groups_mst, distances, points, plot_suffix='_regret')

    # TODO: fill the bodies of local search functions
    # Preparation for local search
    grasp_groups = grasp(points, distances)
    # regret_groups = regret(points, distances)

    # groups = local_search_steep(points, distances)


    # experiment_measurements(local_search_greedy, [grasp_groups, points, distances], sum_all_groups_fully_connected,
                            #distances, points, plot_suffix='_local_search_greedy')

    experiment_measurements(local_search_steep, [grasp_groups, distances], sum_all_groups_fully_connected,
                            distances, points, plot_suffix='_local_search_steep')



main()
