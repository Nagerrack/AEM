from scipy.spatial.distance import euclidean
import numpy as np


def load_points(file_path):
    with open(file_path) as data_file:
        return [[int(number) for number in line.split()] for line in data_file]


def distance_matrix(x, y):
    matrix = np.zeros((len(x), len(y)))
    for i, x_coords in enumerate(x):
        for j, y_coords in enumerate(y):
            matrix[i, j] = euclidean(x_coords, y_coords)
    return matrix
