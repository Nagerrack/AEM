from measurements import experiment_measurements
from measurements import experiment_measurements_parameters

from init_fuction import *
from first_solution_functions import *
from ls_helper import *
from local_searches import *


def main():
    points = load_points(r'data/objects20_06.data')
    distances = distance_matrix(points, points)

    # experiment_measurements(grasp, [points, distances], sum_all_groups_fully_connected, distances, points,
    #                         plot_suffix='_grasp')
    # experiment_measurements(regret, [points, distances], sum_all_groups_mst, distances, points, plot_suffix='_regret')

    # experiment_measurements(local_search_steep, grasp, sum_all_groups_fully_connected,
    #                         distances, points, plot_suffix='_local_search_steep')

    # experiment_measurements(local_search_greedy, random_heuristic,
    # sum_all_groups_fully_connected,
    # distances, points, plot_suffix='local_search_greedy_grasp2')

    # experiment_measurements_parameters(msls, [points, distances], sum_all_groups_fully_connected, distances, points,
    #                                    plot_suffix='_msls3')

    # max_time = 338.1591
    # time 338.1591s
    # print(sum_all_groups_fully_connected(ils_small(20.0, points, distances), distances))

    experiment_measurements_parameters(ils_small, [200.0, points, distances], sum_all_groups_fully_connected, distances,
                                       points,
                                       plot_suffix='_ils_small2')


main()
