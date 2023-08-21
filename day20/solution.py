from os import path


DECRYPTION_KEY = 811589153


def parse_input_file() -> list[int]:
    input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
    return [int(line) for line in input_file.read().strip().splitlines()]


def decrypt_input(input_array: list[int], n=1) -> list[int]:
    indexed_input = list(enumerate(input_array))
    for _ in range(n):
        for i, val in enumerate(input_array):
            index = indexed_input.index((i, val))
            new_index = (index + val) % (len(input_array) - 1)
            index_removed_array = [*indexed_input[:index], *indexed_input[index + 1 :]]
            indexed_input = [
                *index_removed_array[:new_index],
                (i, val),
                *index_removed_array[new_index:],
            ]
    return [i[1] for i in indexed_input]


def solve_part_1() -> int:
    input_array = parse_input_file()
    decrypted = decrypt_input(input_array)
    offset = decrypted.index(0)
    return sum([decrypted[(offset + n) % len(decrypted)] for n in [1000, 2000, 3000]])


def solve_part_2() -> int:
    input_array = [x * DECRYPTION_KEY for x in parse_input_file()]
    decrypted = decrypt_input(input_array, 10)
    offset = decrypted.index(0)
    return sum([decrypted[(offset + n) % len(decrypted)] for n in [1000, 2000, 3000]])


print("Day 20:")
print("Part 1 Solution:  ", solve_part_1())
print("Part 2 Solution:  ", solve_part_2())
