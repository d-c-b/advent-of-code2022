from os import path
import json
from functools import cmp_to_key

input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
input_string = input_file.read().strip()


def parse_input_string_pairs(input: str) -> list[list]:
    pairs_strings = [pair.split("\n") for pair in input.split("\n\n")]
    pairs = [[json.loads(packet) for packet in pair] for pair in pairs_strings]
    return pairs


def parse_input_string_packets(input: str) -> list[list | int]:
    packets = [json.loads(line) for line in input.split("\n") if line]
    return packets


def comparison(left: list | int, right: list | int) -> int:
    if type(left) == int:
        if type(right) == int:
            if left == right:
                return 0
            return 1 if left > right else -1

        if type(right) == list:
            return comparison([left], right)

    if type(left) == list:
        if type(right) == int:
            return comparison(left, [right])
        elif type(right == list):
            assert type(left) == list
            assert type(right) == list
            for l, r in zip(left, right):
                val = comparison(l, r)
                if val != 0:
                    return val
            return comparison(len(left), len(right))

    raise Exception(
        f"Unknown value type, comparison values should be lists or integers, got: {type(left)}, {type(right)}"
    )


def solve_part1() -> int:
    pairs = parse_input_string_pairs(input_string)
    indices_in_right_order = [
        i + 1 for i, pair in enumerate(pairs) if comparison(*pair) < 0
    ]
    return sum(indices_in_right_order)


def solve_part2() -> int:
    divider_packet_1 = [[2]]
    divider_packet_2 = [[6]]
    packet_list = parse_input_string_packets(input_string)
    sorted_packets = sorted(
        [*packet_list, divider_packet_1, divider_packet_2], key=cmp_to_key(comparison)
    )
    return (sorted_packets.index(divider_packet_1) + 1) * (
        sorted_packets.index(divider_packet_2) + 1
    )


print("Day 13:")
print("Part 1 Solution:  ", solve_part1())
print("Part 2 Solution:  ", solve_part2())
