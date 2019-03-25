import random
import networkx as nx
import numpy as np

from ls_helper import average_pair_distances


def get_best_node_move(current_group_id, groups, node, dist_matrix, remote_groups):
    group_nodes = groups[current_group_id].nodes()
    current_average_dist = np.mean(np.array([dist_matrix[node, i] for i in group_nodes]))

    best_move = {'node': node, 'from': current_group_id, 'to': -1, 'profit': 0}

    for i, group in enumerate(groups):
        if remote_groups[current_group_id, i] == True:
            continue
        if i == current_group_id:
            continue

        group_nodes = group.nodes()
        average_dist = np.mean(np.array([dist_matrix[node, i] for i in group_nodes]))

        if (current_average_dist - average_dist) > best_move['profit']:
            best_move['to'] = i
            best_move['profit'] = current_average_dist - average_dist

    return best_move


def get_best_general_move(groups, dist_matrix, remote_groups):
    best_move = {'node': -1, 'from': -1, 'to': -1, 'profit': -1}

    for i, group in enumerate(groups):
        group_nodes = group.nodes()
        for node in group_nodes:
            move = get_best_node_move(i, groups, node, dist_matrix, remote_groups)

            if move['profit'] > best_move['profit']:
                best_move = move

    return best_move


def get_greedy_move(current_group_id, groups, node, dist_matrix):
    group_nodes = groups[current_group_id].nodes()
    current_average_dist = np.mean(np.array([dist_matrix[node, i] for i in group_nodes]))

    move = {'node': node, 'from': current_group_id, 'to': -1, 'profit': 0}

    for i, group in enumerate(groups):
        if i == current_group_id:
            continue

        group_nodes = group.nodes()
        average_dist = np.mean(np.array([dist_matrix[node, i] for i in group_nodes]))

        if (current_average_dist - average_dist) > move['profit']:
            move['to'] = i
            move['profit'] = current_average_dist - average_dist
            return move

    return move


def get_first_profitable_move(groups, dist_matrix):
    best_move = {'node': -1, 'from': -1, 'to': -1, 'profit': -0}

    random.shuffle(groups)
    for i, group in enumerate(groups):
        group_nodes = group.nodes()
        for node in group_nodes:
            move = get_greedy_move(i, groups, node, dist_matrix)
            if move['profit'] > best_move['profit']:
                return move

    return best_move


def determine_remote_groups(groups, dist_matrix):
    remote_groups = np.zeros((len(groups), len(groups)), dtype='bool')

    for i in range(len(groups)):
        current_average = average_pair_distances(groups[i].nodes(), dist_matrix) * 100
        for j in range(i + 1, len(groups)):
            distance_sum = 0
            for node in groups[i]:
                group_nodes = groups[j].nodes()
                distance_sum += np.array([dist_matrix[node, i] for i in group_nodes])

            if current_average < np.mean(distance_sum):
                remote_groups[i, j] = True
                remote_groups[j, i] = True

    return remote_groups


def local_search_steep(groups, dist_matrix):
    best_move = {'node': -1, 'from': -1, 'to': -1, 'profit': 1}

    remote_groups = determine_remote_groups(groups, dist_matrix)
    while best_move['profit'] > 0:
        best_move = get_best_general_move(groups, dist_matrix, remote_groups)
        if best_move['profit'] > 0:
            groups[best_move['from']].remove_node(best_move['node'])
            groups[best_move['to']].add_node(best_move['node'])
    return groups


def get_random_solution(points, groups_number=20):
    groups = [nx.Graph() for _ in range(groups_number)]

    for i in range(len(points)):
        index = random.randint(0, len(groups_number) - 1)
        groups[index].add_node(i)

    return groups


def local_search_greedy(groups, dist_matrix):
    move = {'node': -1, 'from': -1, 'to': -1, 'profit': 1}

    while move['profit'] > 0:
        move = get_first_profitable_move(groups, dist_matrix)
        if move['profit'] > 0:
            groups[move['from']].remove_node(move['node'])
            groups[move['to']].add_node(move['node'])

    return groups
