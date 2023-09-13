from os import path
from collections import defaultdict

ADJACENT_POINTS = (
    (0, -1),
    (0, 1),
    (-1, 0),
    (1, 0),
    (1, -1),
    (-1, -1),
    (-1, 1),
    (1, 1),
)


POSITIONS_TO_CONSIDER = {
    0: [(0, -1), (1, -1), (-1, -1)],  # north
    1: [(0, 1), (1, 1), (-1, 1)],  # south
    2: [(-1, 0), (-1, -1), (-1, 1)],  # west
    3: [(1, 0), (1, -1), (1, 1)],  # east
}


def parse_input_file() -> set[tuple[int, int]]:
    input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
    lines = input_file.read().strip().splitlines()
    elf_positions = set()
    for j, line in enumerate(lines):
        for i, char in enumerate(line):
            if char == "#":
                elf_positions.add((i, j))

    return elf_positions


def perform_diffusion_round(
    elf_positions: set[tuple[int, int]], round_number: int
) -> set[tuple[int, int]]:
    updated_positions = set()
    proposed_positions = defaultdict(list)

    for position_x, position_y in elf_positions:
        if all(
            [
                (position_x + dx, position_y + dy) not in elf_positions
                for (dx, dy) in ADJACENT_POINTS
            ]
        ):
            updated_positions.add((position_x, position_y))
            continue

        for d in range(4):
            direction = (d + round_number) % 4

            if all(
                [
                    (position_x + delta_x, position_y + delta_y) not in elf_positions
                    for delta_x, delta_y in POSITIONS_TO_CONSIDER[direction]
                ]
            ):
                delta_x_prop, delta_y_prop = POSITIONS_TO_CONSIDER[direction][0]
                proposed = position_x + delta_x_prop, position_y + delta_y_prop
                proposed_positions[proposed].append((position_x, position_y))
                break
            if d == 3:
                updated_positions.add((position_x, position_y))

    for proposed, current_positions in proposed_positions.items():
        if len(current_positions) == 1:
            updated_positions.add(proposed)

        else:
            updated_positions.update(current_positions)

    return updated_positions


def solve_part_1() -> int:
    elf_positions = parse_input_file()
    for round_number in range(10):
        elf_positions = perform_diffusion_round(elf_positions, round_number)

    x_vals = [elf_x for elf_x, _ in elf_positions]
    y_vals = [elf_y for _, elf_y in elf_positions]

    width = max(x_vals) - min(x_vals) + 1
    height = max(y_vals) - min(y_vals) + 1
    return (width * height) - len(elf_positions)


def solve_part_2() -> int:

    elf_positions = parse_input_file()
    round_number = 0
    while True:

        updated_positions = perform_diffusion_round(elf_positions, round_number)

        if updated_positions == elf_positions:
            return round_number + 1

        elf_positions = updated_positions
        round_number += 1


print("Day 23:")
print("Part 1 Solution:  ", solve_part_1())
print("Part 2 Solution:  ", solve_part_2())
