

class Node:
    def __init__(self, left_node=None, right_node=None, value=None, nested_tree=None, av_price=None):
        self.left_node = left_node
        self.right_node = right_node
        self.value = value
        self.av_price = av_price
        self.nested_tree = nested_tree

    def __str__(self):
        return str(self.value)

    def add_node(self, new_node):
        if not self.value:
            self.value = new_node.value
            self.nested_tree = new_node.nested_tree
            self.av_price = new_node.av_price

        if new_node.value == self.value:
            return

        if new_node.value < self.value:
            if self.left_node:
                self.left_node.add_node(new_node)
                return
            self.left_node = new_node
            return

        if new_node.value > self.value:
            if self.right_node:
                self.right_node.add_node(new_node)
                return
            self.right_node = new_node
            return

    def search(self, manufacturer: str, year: int) -> float:
        node = self.search_manufacturer(manufacturer)
        if not node:
            return
        return node.nested_tree.search_year(year)

    def search_year(self, year: int):
        if self.value == year:
            return self.av_price

        if year < self.value:
            if not self.left_node:
                return
            return self.left_node.search_year(year)

        if year > self.value:
            if not self.right_node:
                return
            return self.right_node.search_year(year)

    def search_manufacturer(self, manufacturer: str):
        if self.value == manufacturer:
            return self

        if manufacturer < self.value:
            if not self.left_node:
                return
            return self.left_node.search_manufacturer(manufacturer)

        if manufacturer > self.value:
            if not self.right_node:
                return
            return self.right_node.search_manufacturer(manufacturer)
