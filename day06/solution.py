from os import path

input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
input_string = input_file.read().strip()


def find_index_after_n_distinct(n: int) -> int:
    if len(input_string) < n + 1:
        raise Exception("Input string is too short")
    for index in range(len(input_string)):
        if index >= n:
            char_set = set(input_string[index - n : index])
        else:
            continue
        if len(char_set) == n:
            return index
    raise Exception(f"No sequence of {n} distinct characters found in string")


print("Day 06:")
print("Part 1 Solution:  ", find_index_after_n_distinct(4))
print("Part 2 Solution:  ", find_index_after_n_distinct(14))
