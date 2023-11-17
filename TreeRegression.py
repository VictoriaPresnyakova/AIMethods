import math

import numpy as np

from Tree.MyTree import MyTree
from ReadCSV import MyCSV


def count_entr(param: str) -> dict:
    entr = {}
    for i in data_percent[param].unique():
        pi = len(data_percent[data_percent[param] == i]) / len(data_percent)
        entr[i] = - (pi * math.log10(pi))

    entr = dict(sorted(entr.items(), key=lambda x: x[1], reverse=True))
    return entr


my_CSV = MyCSV()
data = my_CSV.data[['Manufacturer', 'Prod. year', 'Price']]

percent = 0.8
data_percent = data.iloc[:int(len(data) * percent)]
other_data = data.iloc[int(len(data) * percent):]

pi_year = count_entr('Prod. year')

# print(len(data_percent))
# print(len(data_percent[data_percent['Manufacturer'] == 'HYUNDAI']))
# print(len(data_percent[data_percent['Manufacturer'] == 'TOYOTA']))


entr_year_sum = 0

pi_manufacturer = count_entr('Manufacturer')
tree = MyTree(data_percent, list(pi_manufacturer.keys()))


d = other_data.groupby(['Manufacturer', 'Prod. year'])['Price'].agg(np.average).reset_index()
print(d)
for i in d.to_numpy():
    print(i[0], i[1], tree.search(i[0], i[1]))
