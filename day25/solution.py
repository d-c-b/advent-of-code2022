from os import path
from collections import defaultdict


def parse_input_file() -> list[str]:
    input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
    lines = input_file.read().strip().splitlines()
    return lines


SNAFU_CHARS_TO_DECIMAL_VALS = {
    "=": -2,
    "-": -1,
    "0": 0,
    "1": 1,
    "2": 2,
}


def sum_snafus(vals: list[str]) -> str:
    position_sums: defaultdict[int, int] = defaultdict(int)

    for val in vals:
        for p, c in enumerate(val[::-1]):
            position_sums[p] += SNAFU_CHARS_TO_DECIMAL_VALS[c]

    snafu_summed = ""
    for i in position_sums:
        q, remainder = divmod(position_sums[i] + 2, 5)
        remainder_char = list(SNAFU_CHARS_TO_DECIMAL_VALS.keys())[remainder]
        snafu_summed = remainder_char + snafu_summed
        if q != 0:
            position_sums[i + 1] += q

    return snafu_summed


def solve_part_1():
    snafus = parse_input_file()
    return sum_snafus(snafus)


print("Day 25:")
print("Part 1 Solution:  ", solve_part_1())
