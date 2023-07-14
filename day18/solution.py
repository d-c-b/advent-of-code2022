from os import path
import re
from typing import cast


def parse_input_file() -> list[tuple[int, int, int]]:
    input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
    coordinates = []
    for line in input_file.read().strip().splitlines():
        if not re.match(r"\d+,\d+,\d+", line):
            raise Exception(f"Invalid input line:  {line}")

        coords = tuple(int(x) for x in line.split(","))
        coords = cast(tuple[int, int, int], coords)

        coordinates.append(coords)
    return coordinates


def neighbour_coords(coords: tuple[int, int, int]) -> list[tuple[int, int, int]]:
    return [
        (coords[0], coords[1], coords[2] + 1),
        (coords[0], coords[1], coords[2] - 1),
        (coords[0], coords[1] + 1, coords[2]),
        (coords[0], coords[1] - 1, coords[2]),
        (coords[0] + 1, coords[1], coords[2]),
        (coords[0] - 1, coords[1], coords[2]),
    ]


def solve_exposed_faces(filled: list[tuple[int, int, int]]) -> int:
    visited = set()
    faces = 0
    for coord in filled:
        visited.add(coord)
        faces += 6
        for neighbour in neighbour_coords(coord):
            if neighbour in visited:
                faces -= 2
    return faces


def solve_part_1() -> int:
    droplet_coords = parse_input_file()
    return solve_exposed_faces(droplet_coords)


def solve_part_2() -> int:
    droplet_coords = parse_input_file()

    min_x, max_x = (
        min([x for x, _, _ in droplet_coords]) - 1,
        max([x for x, _, _ in droplet_coords]) + 1,
    )
    min_y, max_y = (
        min([y for _, y, _ in droplet_coords]) - 1,
        max([y for _, y, _ in droplet_coords]) + 1,
    )
    min_z, max_z = (
        min([z for _, _, z in droplet_coords]) - 1,
        max([z for _, _, z in droplet_coords]) + 1,
    )

    outside_area = set()
    to_visit = [(min_x, min_y, min_z)]
    while to_visit:
        coord = to_visit.pop()
        if coord in outside_area:
            continue

        outside_area.add(coord)
        for neighbour_coord in neighbour_coords(coord):
            if (
                (min_x <= neighbour_coord[0] <= max_x)
                and (min_y <= neighbour_coord[1] <= max_y)
                and (min_z <= neighbour_coord[2] <= max_z)
                and neighbour_coord not in droplet_coords
            ):
                to_visit.append(neighbour_coord)

    all_points_in_range = set(
        (x, y, z)
        for x in range(min_x, max_x + 1)
        for y in range(min_y, max_y + 1)
        for z in range(min_z, max_z + 1)
    )

    filled_droplets = all_points_in_range - outside_area

    return solve_exposed_faces(list(filled_droplets))


print("Day 18:")
print("Part 1 Solution:  ", solve_part_1())
print("Part 2 Solution:  ", solve_part_2())
