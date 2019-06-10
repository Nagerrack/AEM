from genetic import hybrid_genetic
from measurements import experiment_measurements
from measurements import experiment_measurements_parameters

from init_fuction import *
from first_solution_functions import *
from ls_helper import *
from local_searches import *
from similarity_measurement import *


def main():
    points = load_points(r'data/objects20_06.data')
    dist_matrix = distance_matrix(points, points)

    # experiment_measurements(grasp, [points, dist_matrix], sum_all_groups_fully_connected, dist_matrix, points,
    #                         plot_suffix='_grasp')
    # experiment_measurements(regret, [points, dist_matrix], sum_all_groups_mst, dist_matrix, points, plot_suffix='_regret')

    # experiment_measurements(local_search_steep, grasp, sum_all_groups_fully_connected,
    #                         dist_matrix, points, plot_suffix='_local_search_steep')

    # experiment_measurements(local_search_greedy, random_heuristic,
    # sum_all_groups_fully_connected,
    # dist_matrix, points, plot_suffix='local_search_greedy_grasp2')

    # experiment_measurements_parameters(msls, [points, dist_matrix], sum_all_groups_fully_connected, dist_matrix, points,
    # plot_suffix='_msls3')

    # results = get_n_msls_solutions(points, dist_matrix, 250)
    #
    # print("generated")
    # results = fill_best_similarities(results)
    # print("best")
    # results = fill_average_similarities(results)
    # print("average")
    # save_to_file(results)

    max_time = 645.0
    # print(sum_all_groups_fully_connected(hybrid_genetic(points, dist_matrix, max_time), dist_matrix))

    experiment_measurements_parameters(hybrid_genetic, [points, dist_matrix, max_time], sum_all_groups_fully_connected,
                                       dist_matrix, points, plot_suffix='hybrid_genetic_2200')

    # max_time = 338.1591
    # time 338.1591s
    # print(sum_all_groups_fully_connected(ils_small(20.0, points, dist_matrix), dist_matrix))

    # experiment_measurements_parameters(ils_big, [645.0, points, dist_matrix], sum_all_groups_fully_connected, dist_matrix,
    # points,
    # plot_suffix='ils_645big')


main()
