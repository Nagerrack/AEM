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


def experiment_measurements(func, group_generator, aggregate_func, dist_matrix, points, plot_suffix=''):
    start_time = time.time()
    result_dict = {}

    for i in range(1):
        groups = group_generator(points, dist_matrix)
        result, time_elapsed = measure_execution_time_and_result(func, [groups, dist_matrix])
        result_dict[round(aggregate_func(result, dist_matrix), 3)] = (result, time_elapsed)

    max_group, time_elapsed1 = result_dict[max(result_dict)]
    min_group, time_elapsed2 = result_dict[min(result_dict)]
    plot_groups(max_group, points, save=True, name='plots/' + plot_suffix + '_max')
    plot_groups(min_group, points, save=True, name='plots/' + plot_suffix + '_min')

    time_list = [result[1] for result in result_dict.values()]

    print('Min:{0}, {3}s; Max:{1}, {4}s; Average:{2}, {5}s'.format(
        *result_scores(result_dict.keys()),
        round(result_dict[min(result_dict)][1], 4),
        round(result_dict[max(result_dict)][1], 4),
        round(result_scores(time_list)[2], 4)
    ))

    print('Experiment Time: {}s'.format(round(time.time() - start_time, 3)))
    # print('Time:')
    # print('Min:{}, Max:{}, Average:{}', *result_scores([result[1] for result in result_dict.values()]))


def plot_groups(groups, points, save=False, name='figure'):
    colors = ['#f23d55', '#594358', '#4073ff', '#468c62', '#475900', '#d9b8a3', '#8c4646', '#591628', '#d600e6',
              '#6086bf', '#00330e', '#e5da39', '#730f00', '#ff0088', '#2c00a6', '#2d4459', '#435949', '#bf8000',
              '#8c6e69', '#cc99bb', '#4400ff', '#00b8e6', '#007300', '#33260d', '#ffc8bf', '#400033', '#c8bfff',
              '#407b80', '#73e673', '#8c7546', '#e50000', '#ff80e5', '#393973', '#bffbff', '#88ff00', '#4c1f00'
              ]

    color_dict = {i: colors[i] for i in range(len(colors))}

    for i in range(len(groups)):
        for j in groups[i].nodes():
            plt.scatter(*points[j], c=color_dict[i])

    if save:
        plt.savefig(name + '.png')
        plt.show()
    else:
        plt.show()
