from pprint import pprint
from random import randint
import numpy as np

# На языке Python разработайте скрипт, кластеризующий загруженные данные о размере затрат на связь
# среди n отделов на определенные им кластеры,
# обозначенные определенными в программе лингвистическими метками.
# Максимальное количество меток задать самостоятельно.

# (1) инициализация

# лингвистические шкалы
ling_tags = ['очень мало', 'мало', 'средне', 'много', 'очень много']
ling_tags = [[ling_tags[1], ling_tags[3]], ling_tags[1:4], ling_tags[1:5], ling_tags]

# значение целевой функции
J = 0

# степень нечеткости кластеризации
m = 1.6

# уровень точности
e = 0.001

# максимальное кол-во итераций
max_iter = 10000

# кластеры
clasters = np.zeros(randint(2, 5))

# значения объектов
spending = [randint(10, 100) * 1000 for i in range(randint(10, 15))]
print(f'Начальные значения объектов:{spending}')

# матрица принадлежности
belong_matrix = np.zeros([len(spending), len(clasters)])

# рандомно заполняем матрицу принадлежности
for i in range(belong_matrix.shape[0]):
    belong_matrix[i][randint(0, len(belong_matrix[i]) - 1)] = 1

for i in range(max_iter):
    # (2) вычисляем центры кластеров
    for i in range(len(clasters)):
        u_ij = [j ** m for j in belong_matrix[:, i]]

        u_ij_x = [u_ij[k] * spending[k] for k in range(len(u_ij))]

        clasters[i] = sum(u_ij_x) / sum(u_ij)

    # (3) пересчитываем степень принадлежности
    for i in range(belong_matrix.shape[0]):
        for j in range(belong_matrix.shape[1]):
            zn = 0
            for l in clasters:
                if abs(spending[i] - clasters[j]) == 0 or abs(spending[i] - l) == 0:
                    zn = 1
                    break
                zn += ((abs(spending[i] - clasters[j])) / (abs(spending[i] - l))) ** 3.33

            belong_matrix[i][j] = 1 / zn

    # (4) считаем целевую функцию
    new_J = sum([sum([belong_matrix[i][j] ** m * abs(spending[i] - clasters[j]) for i in range(len(spending))]) for j in
                 range(len(clasters))])

    if abs(J - new_J) <= e:
        J = new_J
        break
    J = new_J

clasters.sort()

print(f'Матрица принадлежности:\n{belong_matrix}')

print('Центры кластеров:')
for i in range(len(clasters)):
    print(ling_tags[len(clasters) - 2][i], clasters[i])
