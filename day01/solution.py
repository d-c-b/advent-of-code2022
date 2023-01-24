from os import path

input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
raw_input = input_file.read().strip()

grouped = [
    [int(value) for value in group.split("\n")] for group in raw_input.split("\n\n")
]

summed_groups = [sum(group) for group in grouped]

print("Day 01:")
print("Part 1 Solution:  ", max(summed_groups))
print("Part 2 Solution:  ", sum(sorted(summed_groups)[-3:]))
