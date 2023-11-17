import math

import numpy as np
from pandas import DataFrame

from Tree.MyNode import Node


class MyTree:
    def __init__(self, data: DataFrame, first: list):
        self.first_node = Node()
        nodes = []
        for i in first:
            nodes.append(Node(value=i))

        for i in nodes:

            nodes_for_nested_tree = []
            d = data[data['Manufacturer'] == i.value].groupby(['Prod. year'])['Price'].agg(
                np.average).reset_index().to_numpy()
            for j in d:
                nodes_for_nested_tree.append(Node(value=int(j[0]), av_price=j[1]))
            nodes_for_nested_tree.sort(key=lambda x: -len(data[data['Prod. year'] == x.value])/len(data) *
                                       math.log10(len(data[data['Prod. year'] == x.value])/len(data)), reverse=True)
            i.nested_tree = self.create_nested_tree(nodes_for_nested_tree)
            self.first_node.add_node(i)

    def create_nested_tree(self, nested: list[Node]):
        first_nested = Node()
        for i in nested:
            first_nested.add_node(i)
        return first_nested

    def __str__(self):
        print(f'{self.first_node} \n {self.first_node.left_node}, {self.first_node.right_node}')

    def search(self, manufacturer: str, year: int) -> float:
        return self.first_node.search(manufacturer, year)










