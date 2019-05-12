import copy
import random
import time

import networkx as nx
import numpy as np

from first_solution_functions import grasp, grasp_fully_connected, random_heuristic
from ls_helper import average_pair_distances, sum_all_groups_fully_connected


def get_best_node_move_cache(current_group_id, groups, node, remote_groups, edges_number, profits_cache):
    current_nodes_number = groups[current_group_id].number_of_nodes() - 1

    best_move = {'node': node, 'from': current_group_id, 'to': -1, 'profit': 0, 'egdes': -1}

    for i, group in enumerate(groups):
        if remote_groups[current_group_id, i] == True or i == current_group_id:
            continue

        if profits_cache[node][1][i] > best_move['profit']:
            group_egdes = edges_number + len(group.nodes()) - current_nodes_number

            best_move['to'] = i
            best_move['profit'] = profits_cache[node][1][i]
            best_move['egdes'] = group_egdes

    return best_move


def consists(closest_list, group_nodes):
    for node in closest_list:
        if node[0] in group_nodes:
            return True

    return False


def get_best_node_move_closest(current_group_id, groups, node, dist_matrix, edges_number, closest_groups):
    group_nodes = groups[current_group_id].nodes()
    current_average_dist = np.sum(np.array([dist_matrix[node, i] for i in group_nodes])) / edges_number
    current_nodes_number = groups[current_group_id].number_of_nodes() - 1
    closest_list = closest_groups[node][1]

    best_move = {'node': node, 'from': current_group_id, 'to': -1, 'profit': 0, 'egdes': -1}

    for i, group in enumerate(groups):
        if i == current_group_id:
            continue

        group_nodes = group.nodes()

        if i not in closest_list:
            continue

        group_egdes = edges_number + len(group_nodes) - current_nodes_number
        average_dist = np.sum(np.array([dist_matrix[node, i] for i in group_nodes])) / group_egdes

        if (current_average_dist - average_dist) > best_move['profit']:
            best_move['to'] = i
            best_move['profit'] = current_average_dist - average_dist
            best_move['egdes'] = group_egdes

    return best_move


def get_best_node_move_both(current_group_id, groups, node, edges_number, profits_cache, closest_groups):
    current_nodes_number = groups[current_group_id].number_of_nodes() - 1
    closest_list = closest_groups[node][1]

    best_move = {'node': node, 'from': current_group_id, 'to': -1, 'profit': 0, 'egdes': -1}

    for i, group in enumerate(groups):
        if i not in closest_list:
            continue

        if profits_cache[node][1][i] > best_move['profit']:
            group_egdes = edges_number + len(group.nodes()) - current_nodes_number

            best_move['to'] = i
            best_move['profit'] = profits_cache[node][1][i]
            best_move['egdes'] = group_egdes

    return best_move


def get_best_node_move(current_group_id, groups, node, dist_matrix, remote_groups, edges_number):
    group_nodes = groups[current_group_id].nodes()
    current_average_dist = np.sum(np.array([dist_matrix[node, i] for i in group_nodes])) / edges_number
    current_nodes_number = groups[current_group_id].number_of_nodes() - 1

    best_move = {'node': node, 'from': current_group_id, 'to': -1, 'profit': 0, 'egdes': -1}

    for i, group in enumerate(groups):
        if remote_groups[current_group_id, i] == True:
            continue
        if i == current_group_id:
            continue

        group_nodes = group.nodes()
        group_egdes = edges_number + len(group_nodes) - current_nodes_number
        average_dist = np.sum(np.array([dist_matrix[node, i] for i in group_nodes])) / group_egdes

        if (current_average_dist - average_dist) > best_move['profit']:
            best_move['to'] = i
            best_move['profit'] = current_average_dist - average_dist
            best_move['egdes'] = group_egdes

    return best_move


def get_best_general_move(groups, dist_matrix, remote_groups, edges_number, profits_cache, closest_groups):
    best_move = {'node': -1, 'from': -1, 'to': -1, 'profit': -1, 'edges': -1}

    for i, group in enumerate(groups):
        group_nodes = group.nodes()
        for node in group_nodes:
            # move = get_best_node_move(i, groups, node, dist_matrix, remote_groups, edges_number)
            # move = get_best_node_move_cache(i, groups, node, remote_groups, edges_number, profits_cache)
            # move = get_best_node_move_closest(i, groups, node, dist_matrix, edges_number, closest_groups)
            move = get_best_node_move_both(i, groups, node, edges_number, profits_cache, closest_groups)

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
    best_move = {'node': -1, 'from': -1, 'to': -1, 'profit': 0}

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


def determine_closest_nodes(current_group_id, current_node, dist_matrix, groups):
    closest = []

    for i, group in enumerate(groups):
        group_nodes = group.nodes()

        for node in group_nodes:
            if i == current_group_id:
                closest.append([i, 99999])
            else:
                closest.append([i, dist_matrix[current_node, node]])

    return sorted(closest, key=lambda l: l[1])[:100]


def determine_all_closest_nodes(dist_matrix, groups):
    closest = []

    for i, group in enumerate(groups):
        group_nodes = group.nodes()
        for node in group_nodes:
            closest_groups = determine_closest_nodes(i, node, dist_matrix, groups)
            closest_g = [x[0] for x in closest_groups]
            closest.append([node, closest_g])

    return sorted(closest, key=lambda l: l[0])


def get_move_profits(current_group_id, groups, node, dist_matrix, edges_number):
    profits = []
    group_nodes = groups[current_group_id].nodes()
    current_average_dist = np.sum(np.array([dist_matrix[node, i] for i in group_nodes])) / edges_number
    current_nodes_number = groups[current_group_id].number_of_nodes() - 1

    for i, group in enumerate(groups):
        if i == current_group_id:
            profits.append(0)
            continue

        group_nodes = group.nodes()
        group_egdes = edges_number + len(group_nodes) - current_nodes_number
        average_dist = np.sum(np.array([dist_matrix[node, i] for i in group_nodes])) / group_egdes

        profits.append((current_average_dist - average_dist))

    return profits


def cache_profits(groups, dist_matrix, edges_number):
    cache = []

    for i, group in enumerate(groups):
        group_nodes = group.nodes()
        for node in group_nodes:
            cache.append([node, get_move_profits(i, groups, node, dist_matrix, edges_number)])

    return sorted(cache, key=lambda l: l[0])


def update_cache(profits_cache, groups, groups_to_change, dist_matrix, edges_number):
    for i in groups_to_change:
        group_nodes = groups[i].nodes()
        for node in group_nodes:
            profits_cache[node] = [node, get_move_profits(i, groups, node, dist_matrix, edges_number)]

    return profits_cache


def get_egdes_number(groups):
    edges = 0

    for group in groups:
        group_nodes = group.nodes()
        nodes_count = len(group_nodes)
        edges += (nodes_count * (nodes_count - 1)) / 2

    return edges


def local_search_steep(groups, dist_matrix):
    best_move = {'node': -1, 'from': -1, 'to': -1, 'profit': 1, 'edges': -1}
    edges_number = get_egdes_number(groups)
    profits_cache = cache_profits(groups, dist_matrix, edges_number)
    closest_groups = determine_all_closest_nodes(dist_matrix, groups)

    remote_groups = determine_remote_groups(groups, dist_matrix)
    while best_move['profit'] > 0:
        best_move = get_best_general_move(groups, dist_matrix, remote_groups, edges_number, profits_cache,
                                          closest_groups)
        if best_move['profit'] > 0:
            groups[best_move['from']].remove_node(best_move['node'])
            groups[best_move['to']].add_node(best_move['node'])
            edges_number = best_move['egdes']
            profits_cache = update_cache(profits_cache, groups, [best_move['from'], best_move['to']], dist_matrix,
                                         edges_number)

    return groups


def get_random_solution(points, groups_number=20):
    groups = [nx.Graph() for _ in range(groups_number)]

    for i in range(len(points)):
        index = random.randint(0, groups_number - 1)
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


def msls(points, dist_matrix):
    result_dict = {}

    for i in range(100):
        groups = random_heuristic(points, dist_matrix)
        groups = local_search_steep(groups, dist_matrix)
        result_dict[sum_all_groups_fully_connected(groups, dist_matrix)] = groups

    return result_dict[min(result_dict)]


def get_time(timepoint):
    return time.time() - timepoint


def ils_small(max_time, points, dist_matrix):
    timepoint = time.time()
    groups = random_heuristic(points, dist_matrix)
    previous_groups = local_search_steep(groups, dist_matrix)
    swap_number = random.randint(2, 10)
    while get_time(timepoint) < max_time:
        # print(get_time(timepoint))
        new_groups = swap_points(swap_number, copy.deepcopy(previous_groups))
        new_groups = local_search_steep(new_groups, dist_matrix)
        if (sum_all_groups_fully_connected(new_groups, dist_matrix) <
                sum_all_groups_fully_connected(previous_groups, dist_matrix)):
            if swap_number > 1:
                swap_number -= 1
            previous_groups = new_groups
        else:
            if swap_number < int(len(points) * 0.1):
                swap_number += 1
        # print(swap_number)
    return previous_groups


def ils_big(max_time, points, dist_matrix):
    timepoint = time.time()
    groups = random_heuristic(points, dist_matrix)
    previous_groups = local_search_steep(groups, dist_matrix)
    destroy_number = random.randint(int(len(points) * 0.1), int(len(points) * 0.3))
    while get_time(timepoint) < max_time:
        new_groups, deleted = destroy(copy.deepcopy(previous_groups), destroy_number)
        new_groups = repair(new_groups, deleted, dist_matrix)
        new_groups = local_search_steep(new_groups, dist_matrix)
        if (sum_all_groups_fully_connected(new_groups, dist_matrix) <
                sum_all_groups_fully_connected(previous_groups, dist_matrix)):
            previous_groups = new_groups
    return previous_groups


def swap_points(swap_number, groups):
    for i in range(swap_number):
        group1_number = random.randrange(len(groups))
        group2_number = random.randrange(len(groups))
        group1 = groups[group1_number]
        group2 = groups[group2_number]
        nodes1 = groups[group1_number].nodes()
        node1_index = random.randrange(len(groups[group1_number].nodes()))
        node1 = list(nodes1.keys())[node1_index]
        group1.remove_node(node1)
        group2.add_node(node1)
    return groups


def destroy(groups, destroy_number):
    deleted = []
    for i in range(destroy_number):
        flag = 0
        while flag < 1:
            group_index = random.randrange(len(groups))
            group = groups[group_index]
            nodes = group.nodes()
            flag = len(nodes)
        node_index = random.randrange(len(nodes))
        node = list(nodes.keys())[node_index]
        group.remove_node(node)
        deleted.append(node)
    return groups, deleted


def repair(groups, points_left, dist_matrix):
    return grasp_fully_connected(points_left, groups, dist_matrix)
