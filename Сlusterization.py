import copy
import random
from pprint import pprint

import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np

from ReadCSV import MyCSV

#перераспределение центров кластеров по привязанным к ним точкам
def cluster_update(cluster, cluster_content, dim):
    k = len(cluster)
    for i in range(k):  # по i кластерам
        for q in range(dim):  # по q параметрам
            updated_parameter = 0
            for j in range(len(cluster_content[i])):
                updated_parameter += cluster_content[i][j][q]
            if len(cluster_content[i]) != 0:
                updated_parameter = updated_parameter / len(cluster_content[i])
            cluster[i][q] = updated_parameter
    return cluster


#первичное распределения точек по кластерам
def data_distribution(array, cluster, k, n, dim):
    cluster_content = [[] for i in range(k)]

    for i in range(n):
        min_distance = float('inf')
        situable_cluster = -1
        for j in range(k):
            distance = 0
            for q in range(dim):
                distance += (array[i][q] - cluster[j][q]) ** 2

            distance = distance ** (1 / 2)
            if distance < min_distance:
                min_distance = distance
                situable_cluster = j

        cluster_content[situable_cluster].append(array[i])

    return cluster_content


def clusterization(array, k):
    n = len(array)
    dim = len(array[0]) #двумерное
    max_cluster_value = max(max(array))
    cluster = [[0 for i in range(dim)] for q in range(k)] #центры кластеров
    cluster_content = [[] for i in range(k)] #массивов точек принадлежащих соответствующему кластеру.

    for i in range(dim):
        for q in range(k):
            cluster[q][i] = random.randint(0, max_cluster_value) #первичные центры кластеров

    cluster_content = data_distribution(array, cluster, k, n, dim)

    privious_cluster = copy.deepcopy(cluster)
    while 1:
        cluster = cluster_update(cluster, cluster_content, dim)
        cluster_content = data_distribution(array, cluster, k, n, dim)
        # пока пересчёт центров кластеров будет приносить плоды
        if cluster == privious_cluster:
            break
        privious_cluster = copy.deepcopy(cluster)
    #pprint(cluster_content)
    return cluster_content


def visualisation_2d(cluster_content):
    k = len(cluster_content)
    plt.grid()
    plt.xlabel("x")
    plt.ylabel("y")

    for i in range(k):
        x_coordinates = []
        y_coordinates = []
        for q in range(len(cluster_content[i])):
            x_coordinates.append(cluster_content[i][q][0])
            y_coordinates.append(cluster_content[i][q][1])
        plt.scatter(x_coordinates, y_coordinates)
    plt.show()

my_csv = MyCSV()
data = my_csv.data[['Prod. year', 'Price']]
for i in range(100):
    data = data[data['Price'] != data['Price'].max()]
data = data.to_numpy()
arr = [[i[0], i[1]] for i in data if i[0] != data.max() and i[1] != data.max()]
visualisation_2d(clusterization(arr, 5))
