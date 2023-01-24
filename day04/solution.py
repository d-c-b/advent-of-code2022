from os import path

input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
lines = input_file.read().strip().splitlines()


def range_is_enclosed(range1: list[int], range2: list[int]) -> bool:
    if range1[0] <= range2[0] and range1[1] >= range2[1]:
        return True
    if range2[0] <= range1[0] and range2[1] >= range1[1]:
        return True
    return False


def ranges_overlap(range1: list[int], range2: list[int]) -> bool:
    if range1[0] <= range2[0] and range1[1] >= range2[0]:
        return True
    if range2[0] <= range1[0] and range2[1] >= range1[0]:
        return True
    return False


def validate_range(range: list[list[int]]):
    if len(range) != 2:
        raise Exception(f"One or more invalid ranges: {range}")
    return range


range_pairs = list(
    map(
        validate_range,
        [
            [[int(x) for x in range.split("-")] for range in line.split(",")]
            for line in lines
        ],
    )
)


fully_enclosed_pair_count = sum(
    [range_is_enclosed(range1, range2) for range1, range2 in range_pairs]
)
overlapping_count = sum(
    [ranges_overlap(range1, range2) for range1, range2 in range_pairs]
)

print("Day 04:")
print("Part 1 Solution:  ", fully_enclosed_pair_count)
print("Part 2 Solution:  ", overlapping_count)
