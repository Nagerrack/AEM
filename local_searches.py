import random
import networkx as nx
import numpy as np

from ls_helper import average_pair_distances

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
        best_move = get_best_general_move(groups, dist_matrix, remote_groups, edges_number, profits_cache, closest_groups)
        if best_move['profit'] > 0:
            groups[best_move['from']].remove_node(best_move['node'])
            groups[best_move['to']].add_node(best_move['node'])
            edges_number = best_move['egdes']
            profits_cache = update_cache(profits_cache, groups, [best_move['from'], best_move['to']], dist_matrix, edges_number)

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
