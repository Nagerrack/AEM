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


# append a sequence of MSTs with a sequence of points
def append_sequence(groups, sequence, dist_matrix):
    for group, point in sequence:
        append_mst(groups[group], point, dist_matrix)
