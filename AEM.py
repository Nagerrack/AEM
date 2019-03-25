from measurements import experiment_measurements

from init_fuction import *
from first_solution_functions import *
from ls_helper import *
from local_searches import *


def main():
    points = load_points(r'data/objects20_06.data')
    distances = distance_matrix(points, points)
    # experiment_measurements(grasp, [points, distances], sum_all_groups_fully_connected, distances, points, plot_suffix='_grasp')
    # experiment_measurements(regret, [points, distances], sum_all_groups_mst, distances, points, plot_suffix='_regret')

    experiment_measurements(local_search_steep, grasp, sum_all_groups_fully_connected,
                            distances, points, plot_suffix='_local_search_steep')

    # experiment_measurements(local_search_greedy, random_heuristic,
                            # sum_all_groups_fully_connected,
                            # distances, points, plot_suffix='local_search_greedy_grasp2')


main()
