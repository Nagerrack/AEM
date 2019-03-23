import time

import matplotlib.pyplot as plt


def result_scores(result_list):
    return round(min(result_list), 4), round(max(result_list), 4), round(sum(result_list) / len(result_list), 4)


def measure_execution_time_and_result(func, parameters):
    start = time.time()
    result = func(*parameters)
    stop = time.time()
    time_elapsed = stop - start
    # print(time_elapsed)
    return result, time_elapsed


def experiment_measurements(func, parameters, aggregate_func, dist_matrix, points):
    result_dict = {}
    for i in range(100):
        result, time_elapsed = measure_execution_time_and_result(func, parameters)
        result_dict[round(aggregate_func(result, dist_matrix), 3)] = (result, time_elapsed)

    max_group, time_elapsed1 = result_dict[max(result_dict)]
    min_group, time_elapsed2 = result_dict[min(result_dict)]
    plot_groups(max_group, points, save=True, name='MaxFigure')
    plot_groups(min_group, points, save=True, name='MinFigure')

    time_list = [result[1] for result in result_dict.values()]

    print('Min:{0}, {3}s; Max:{1}, {4}s; Average:{2}, {5}s'.format(
        *result_scores(result_dict.keys()),
        round(result_dict[min(result_dict)][1], 4),
        round(result_dict[max(result_dict)][1], 4),
        round(result_scores(time_list)[2], 4)
    ))
    # print('Time:')
    # print('Min:{}, Max:{}, Average:{}', *result_scores([result[1] for result in result_dict.values()]))


def plot_groups(groups, points, save=False, name='figure'):
    colors = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#00FFFF',
              '#FF00FF', '#FF8C00', '#696969', '#7B68EE', '#7FFFD4', '#008080']

    color_dict = {i: colors[i] for i in range(len(colors))}

    for i in range(len(groups)):
        for j in groups[i].nodes():
            plt.scatter(*points[j], c=color_dict[i])

    if save:
        plt.savefig(name + '.png')
        plt.show()
    else:
        plt.show()
