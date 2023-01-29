from os import path

input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
lines = input_file.read().strip().splitlines()


class Node:
    def __init__(self, parent, children, label, value, is_directory):
        self.parent = parent
        self.children = children
        self.label = label
        self.value = value
        self.is_directory = is_directory

    def calculate_value_for_directory(self):
        value = 0
        for child in self.children:
            if child.is_directory:
                value += child.calculate_value_for_directory()

            else:
                value += child.value
        self.value = value
        return value

    def get_directory_nodes_size_up_to(self, max_size):
        dirs_size_up_to_max = []
        for child in self.children:
            if child.is_directory:
                if child.value <= max_size:
                    dirs_size_up_to_max.append(child)

                dirs_size_up_to_max += child.get_directory_nodes_size_up_to(max_size)

        return dirs_size_up_to_max

    def get_sizes_of_all_directories(self):
        dir_sizes = []
        for child in self.children:
            if child.is_directory:
                dir_sizes.append(child.value)
                dir_sizes += child.get_sizes_of_all_directories()
        return dir_sizes


def build_tree():
    root_node = Node(parent=None, children=[], label="/", value=0, is_directory=True)
    current = root_node
    for line in lines:
        if line.startswith("$ cd"):
            if line[5:] == "..":
                current = current.parent
            else:
                if line[5:] == "/":
                    current = root_node
                else:
                    (current,) = [
                        child for child in current.children if child.label == line[5:]
                    ]

        elif line.startswith("$ ls"):
            continue

        else:
            value, label = line.split()
            if value == "dir":
                current.children.append(
                    Node(
                        parent=current,
                        children=[],
                        label=label,
                        value=0,
                        is_directory=True,
                    )
                )
            else:
                current.children.append(
                    Node(
                        parent=current,
                        children=None,
                        label=label,
                        value=int(value),
                        is_directory=False,
                    )
                )

    return root_node


root = build_tree()
root.calculate_value_for_directory()

MAX_SIZE = 100000


UNUSED_SPACE = 70000000 - root.value
MIN_TO_DELETE = 30000000 - UNUSED_SPACE


print("Day 07:")
print(
    "Part 1 Solution:  ",
    sum([node.value for node in root.get_directory_nodes_size_up_to(MAX_SIZE)]),
)
print(
    "Part 2 Solution:  ",
    min(filter(lambda x: x > MIN_TO_DELETE, root.get_sizes_of_all_directories())),
)
