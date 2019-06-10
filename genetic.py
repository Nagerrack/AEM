import copy
import random
import time

import networkx as nx
import numpy as np

from first_solution_functions import grasp, random_heuristic, init_groups
from local_searches import local_search_steep, get_time, local_search_greedy
from ls_helper import sum_all_groups_fully_connected


def get_solution(points, dist_matrix):
    groups = random_heuristic(points, dist_matrix)
    solution = local_search_steep(groups, dist_matrix)
    # print(1)
    return solution


def random_fill(groups, points_left, group_number=20):
    for point in points_left:
        groups[random.randint(0, group_number - 1)].add_node(point)

    return groups


def get_worst_sample(population, dist_matrix):
    sample_dict = {round(sum_all_groups_fully_connected(sample, dist_matrix), 8): index
                   for index, sample in enumerate(population)}
    return sample_dict[max(sample_dict)], max(sample_dict)


def max_similar_group(group, sample):
    similarity_dict = {len(set(group) & set(g.nodes())): (index, list(g.nodes()))
                       for index, g in enumerate(sample)}
    return similarity_dict[max(similarity_dict)]


def recombination(point_number, parent_a: list, parent_b: list, groups_number=20):
    parent_b = copy.deepcopy(parent_b)
    points_left = set(range(point_number))
    # zainicjalizuj nowe grupy
    groups = [nx.Graph() for _ in range(groups_number)]
    # dla każdej grupy w rodzicu A
    for index, group_a in enumerate(parent_a):
        # znajdź najbardziej podobną grupę w rodzicu B
        index_b, group_b = max_similar_group(group_a.nodes(), parent_b)
        # pobierz część wspólną
        intersect = set(group_a.nodes()) & set(group_b)
        # usuń ją spośród pozostałych punktów
        points_left = points_left - intersect
        # dodaj część wspólną grup do potomka
        groups[index].add_nodes_from(intersect)
        # usuń grupę z rodzica B
        parent_b.pop(index_b)

    # uzupełnij rozwiązanie losowo przypisując pozostałe punkty
    return random_fill(groups, points_left)


def hybrid_genetic(points, dist_matrix, max_time, population_size=15):
    timepoint = time.time()
    # zasil populację zadaną ilością rozwiązań o losowym punkcie startowym
    population = [get_solution(points, dist_matrix) for _ in range(population_size)]
    iterations = population_size

    while get_time(timepoint) < max_time:
        # dokonaj rekombinacji na podstawie dwóch losowo wybranych rodziców
        parent_indices = np.random.choice(population_size, 2, replace=False)
        # print(parent_indices)
        new_sample = recombination(len(points), *[population[ind] for ind in parent_indices])
        # wykonaj przeszukiwanie lokalne
        new_sample = local_search_steep(new_sample, dist_matrix)

        # uzyskaj indeks oraz wartość funkcji celu dla najgorszego osobnika z populacji
        index, worst_sample_score = get_worst_sample(population, dist_matrix)

        new_sample_score = sum_all_groups_fully_connected(new_sample, dist_matrix)

        # jeśli nowy osobnik ma niższą wartość funkcji niż najgorszy osobnik
        # dotychczasowej populacji - dodaj nowego osobnika oraz usuń starego
        if new_sample_score < worst_sample_score \
                and all(score != new_sample_score for score in
                        [sum_all_groups_fully_connected(sampl, dist_matrix) for sampl in population]):
            population[index] = new_sample

        iterations += 1

    # po przekroczeniu zadanej ilości czasu wykonaj selekcję elitarną by wyłonić najlepszego osobnika z populacji
    result_dict = {round(sum_all_groups_fully_connected(sample, dist_matrix), 8): sample for sample in population}
    print(iterations)

    return result_dict[min(result_dict)]
