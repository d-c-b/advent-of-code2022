from os import path
import re
from typing import cast


def parse_input_file() -> list[tuple[tuple[int, int], tuple[int, int]]]:
    input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
    lines = input_file.read().strip().splitlines()
    input_list = []
    for line in lines:
        sensor, nearest_beacon = line.split(":")
        sensor_coords = tuple([int(i) for i in re.findall(r"-?\d+", sensor)])
        nearest_beacon_coords = tuple(
            [int(i) for i in re.findall(r"-?\d+", nearest_beacon)]
        )
        assert len(sensor_coords) == len(nearest_beacon_coords) == 2
        sensor_coords = cast(tuple[int, int], sensor_coords)
        nearest_beacon_coords = cast(tuple[int, int], nearest_beacon_coords)
        input_list.append((sensor_coords, nearest_beacon_coords))

    return input_list


def manhatten_dist(coords1: tuple[int, int], coords2: tuple[int, int]) -> int:
    x1, y1 = coords1
    x2, y2 = coords2
    return abs(y1 - y2) + abs(x1 - x2)


def calculate_excluded_ranges(
    input_list: list[tuple[tuple[int, int], tuple[int, int]]], row_number: int
) -> list[tuple[int, int]]:
    excluded_ranges = []
    for sensor_coords, nearest_beacon_coords in input_list:
        sensor_x, sensor_y = sensor_coords
        dist = manhatten_dist(sensor_coords, nearest_beacon_coords)
        y_diff = abs(sensor_y - row_number)
        if y_diff < dist:
            x_diff = dist - y_diff
            excluded_ranges.append((sensor_x - x_diff, sensor_x + x_diff))

    return excluded_ranges


def ranges_overlap(range1: tuple[int, int], range2: tuple[int, int]) -> bool:
    start1, end1 = range1
    start2, end2 = range2
    if (start1 <= end2 and start2 <= end1) or (start1 <= start1 and end1 >= end2):
        return True
    return False


def combine_overlapping_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if len(ranges) == 0:
        return []

    sorted_ranges = sorted(ranges)
    combined = []
    current_range = sorted_ranges[0]
    for range in sorted_ranges[1:]:
        if ranges_overlap(current_range, range):
            current_range = (current_range[0], max(range[1], current_range[1]))
        else:
            combined.append(((current_range[0], max(current_range[1], range[1]))))
            current_range = range

    combined.append((current_range[0], max(current_range[1], range[1])))
    return combined


def solve_part_1(row_y: int) -> int:
    input_list = parse_input_file()

    beacons = set(
        [beacon_coords for _, beacon_coords in input_list if beacon_coords[1] == row_y]
    )

    excluded_ranges = calculate_excluded_ranges(input_list, row_y)
    combined = combine_overlapping_ranges(excluded_ranges)

    return sum([range[1] + 1 - range[0] for range in combined]) - len(beacons)


def get_border_coordinates(sensor_coords: tuple[int, int], radius: int):
    sensor_x, sensor_y = sensor_coords
    for i in range(0, radius + 2):
        yield sensor_x + i, sensor_y + radius + 1 - i
        yield sensor_x + i, sensor_y - (radius + 1 - i)

    for i in range(-radius - 1, 0):
        yield sensor_x + i, sensor_y + (radius + i + 1)
        yield sensor_x + i, sensor_y - (radius + i + 1)


def coord_is_excluded_by_a_sensor(coord: tuple[int, int], input_list) -> bool:
    for s, b in input_list:
        if manhatten_dist(coord, s) <= manhatten_dist(s, b):
            return True
    return False


def solve_part_2(max_coord_value: int) -> int:
    input_list = parse_input_file()

    for input in input_list:
        sensor_coords, nearest_beacon_coords = input
        distance = manhatten_dist(sensor_coords, nearest_beacon_coords)

        for coord in get_border_coordinates(sensor_coords, distance):
            x, y = coord
            if x < 0 or x > max_coord_value or y < 0 or y > max_coord_value:
                continue
            if not coord_is_excluded_by_a_sensor(coord, input_list):
                return x * 4000000 + y

    return -1


print("Day 15:")
print("Part 1 Solution:  ", solve_part_1(2000000))
print("Part 2 Solution:  ", solve_part_2(4000000))
