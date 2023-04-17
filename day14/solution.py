from os import path
from typing import cast

SAND_SOURCE_COORDS = (500, 0)


def parse_input_lines() -> list[list[tuple[int, int]]]:
    input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
    lines = input_file.read().strip().splitlines()
    rock_coords = []
    for line in lines:
        line = line.replace(" ", "")
        coords = cast(
            list[tuple[int, int]],
            [tuple(map(int, c.split(","))) for c in line.split("->")],
        )
        rock_coords.append(coords)

    return rock_coords


def get_filled_coordinates_from_rock_coordinates(
    rock_coords: list[list[tuple[int, int]]]
) -> set[tuple[int, int]]:
    filled_coords = set()
    for rock_line in rock_coords:
        for (start_x, start_y), (end_x, end_y) in zip(rock_line, rock_line[1:]):
            if start_x == end_x:
                for y in range(min(start_y, end_y), max(start_y, end_y) + 1):
                    filled_coords.add((start_x, y))

            elif start_y == end_y:
                for x in range(min(start_x, end_x), max(start_x, end_x) + 1):
                    filled_coords.add((x, start_y))

    return filled_coords


def solve(
    filled_coords: set[tuple[int, int]], break_condition, floor_y: int | None = None
) -> int:
    i = 0
    sand_x, sand_y = SAND_SOURCE_COORDS
    while True:
        if (sand_x, sand_y + 1) not in filled_coords:
            sand_y += 1

        elif (sand_x, sand_y + 1) in filled_coords:
            if (sand_x - 1, sand_y + 1) not in filled_coords:
                sand_x, sand_y = sand_x - 1, sand_y + 1

            elif (sand_x + 1, sand_y + 1) not in filled_coords:
                sand_x, sand_y = sand_x + 1, sand_y + 1

            else:
                filled_coords.add((sand_x, sand_y))
                i += 1
                sand_x, sand_y = SAND_SOURCE_COORDS

        if break_condition(sand_x, sand_y):
            break

        if floor_y and sand_y == floor_y:
            filled_coords.add((sand_x, sand_y))
            sand_x, sand_y = SAND_SOURCE_COORDS

    return i


def solve1(rock_coords: list[list[tuple[int, int]]]) -> int:
    filled_coords = get_filled_coordinates_from_rock_coordinates(rock_coords)
    Y_MAX = max([y for _, y in filled_coords])
    break_condition = lambda _, y: y > Y_MAX
    return solve(
        filled_coords=filled_coords,
        break_condition=break_condition,
    )


def solve2(rock_coords: list[list[tuple[int, int]]]) -> int:
    filled_coords = get_filled_coordinates_from_rock_coordinates(rock_coords)
    Y_MAX = max([y for _, y in filled_coords])
    break_condition = lambda *_: SAND_SOURCE_COORDS in filled_coords
    return solve(
        filled_coords=filled_coords, break_condition=break_condition, floor_y=Y_MAX + 2
    )


rock_coords = parse_input_lines()


print("Day 14:")
print("Part 1 Solution:  ", solve1(rock_coords))
print("Part 2 Solution:  ", solve2(rock_coords))
