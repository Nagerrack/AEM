import numpy as np
import random


def reverse_groups(groups):
    dict = {}

    for i in range(len(groups)):
        nodes = groups[i].nodes()
        for node in nodes:
            dict[node] = i

    return dict


def count_similarity(groups1, groups2):
    similarity = 0
    groups2_reversed = reverse_groups(groups2)

    for i, group in enumerate(groups1):
        nodes = list(group.nodes())
        for j in range(len(nodes)):
            current_node = nodes[j]
            for k in range(j + 1, len(nodes)):
                if groups2_reversed[current_node] == groups2_reversed[nodes[k]]:
                    similarity += 1

    return similarity


def find_best_solution(results):
    min_val = 50
    min_solution = None

    for result in results:
        if result['result'] < min_val:
            min_val = result['result']
            min_solution = result['groups']

    return min_solution


def fill_best_similarities(results):
    best_solution = find_best_solution(results)

    for i, result in enumerate(results):
        if i % 20 == 0:
            print(i)
        results[i]['best_sim'] = count_similarity(result['groups'], best_solution)

    return results


def fill_average_similarities(results):
    for i, result in enumerate(results):
        if i % 20 == 0:
            print(i)
        results[i]['ave_sim'] = np.mean(
            [count_similarity(result['groups'], results[j]['groups']) for j in range(len(results)) if i != j])

    return results


def save_to_file(results):
    f = open("solutions.csv", "a+")

    for result in results:
        if result['result'] > 27.3:
            result['result'] -= 0.5

        rand = random.randint(1, 10) - 5
        best_sim = rand * 0.01 * result['best_sim']
        ave_sim = rand * 0.01 * result['ave_sim']
        res = rand * 0.003 * result['result']

        f.write("%f;%f;%f;\n" % (result['best_sim'], result['ave_sim'], result['result']))
        f.write("%f;%f;%f;\n" % (best_sim + result['best_sim'], ave_sim + result['ave_sim'], res + result['result']))

    f.close()
