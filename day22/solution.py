from os import path
import re


DIRECTIONS_MAP = {
    0: (1, 0),  # RIGHT
    1: (0, 1),  # DOWN
    2: (-1, 0),  # LEFT
    3: (0, -1),  # UP
}


ZIP_DIRECTIONS_MAP = {
    (1, 1): [0, 1],
    (-1, 1): [1, 2],
    (-1, -1): [2, 3],
    (1, -1): [3, 0],
}


ADJACENT_POINTS = [
    (1, 0),
    (1, -1),
    (0, -1),
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, 1),
    (1, 1),
]


def parse_input_file() -> tuple[dict[tuple[int, int], str], list[int | str]]:
    input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
    map, instructions_string = input_file.read().split("\n\n")
    board = {}
    for j, line in enumerate(map.splitlines()):
        for i, char in enumerate(line):
            if char in [".", "#"]:
                board[(i, j)] = char

    instructions = [
        int(x) if x.isdigit() else x
        for x in re.findall(r"\d+|[L|R]", instructions_string)
    ]

    return board, instructions


def get_new_position_wrap_around(
    position_x: int, position_y: int, direction: int, board: dict[tuple[int, int], str]
) -> tuple[int, int]:
    new_position = (
        position_x + DIRECTIONS_MAP[direction][0],
        position_y + DIRECTIONS_MAP[direction][1],
    )
    if new_position in board:
        return new_position

    new_x, new_y = new_position
    if direction in [0, 2]:
        min_x, max_x = min([x for x, y in board if y == position_y]), max(
            [x for x, y in board if y == position_y]
        )
        new_x = ((new_x - min_x) % (max_x - min_x + 1)) + min_x
        new_y = position_y
        return (new_x, new_y)

    else:
        min_y, max_y = min([y for x, y in board if x == position_x]), max(
            [y for x, y in board if x == position_x]
        )
        new_y = ((new_y - min_y) % (max_y - min_y + 1)) + min_y
        new_x = position_x
        return (new_x, new_y)


def get_new_position_wrap_around_cube(
    position_x: int,
    position_y: int,
    direction: int,
    board: dict[tuple[int, int], str],
    mapping: dict[tuple[tuple[int, int], int], tuple[tuple[int, int], int]],
) -> tuple[tuple[int, int], int]:
    new_position = (
        position_x + DIRECTIONS_MAP[direction][0],
        position_y + DIRECTIONS_MAP[direction][1],
    )
    if new_position in board:
        return new_position, direction

    new_position, new_direction = mapping[(position_x, position_y), direction]

    return new_position, new_direction


def solve_part_1() -> int:
    board, instructions = parse_input_file()
    direction = 0

    position = (min([x for x, y in board if y == 0 and board[(x, y)] == "."]), 0)

    for instruction in instructions:
        if isinstance(instruction, int):
            for _ in range(instruction):
                new_x, new_y = get_new_position_wrap_around(*position, direction, board)

                if board.get((new_x, new_y)) == ".":
                    position = (new_x, new_y)
                elif board.get((new_x, new_y)) == "#":
                    break

        else:
            match instruction:
                case "R":
                    direction = (direction + 1) % 4
                case "L":
                    direction = (direction - 1) % 4
                case _:
                    raise Exception(f"Invalid instruction in input: {instruction}")

    position_x, position_y = position

    return 1000 * (position_y + 1) + 4 * (position_x + 1) + direction


def check_if_inner_corner(
    coords: tuple[int, int], board: dict[tuple[int, int], str]
) -> tuple[bool, list[int]]:
    x, y = coords

    free_adjacent_points = [
        (dx, dy) for dx, dy in ADJACENT_POINTS if (x + dx, y + dy) not in board
    ]

    if len(free_adjacent_points) == 1:
        free_adjacent_point = free_adjacent_points[0]
        directions_to_zip = ZIP_DIRECTIONS_MAP.get(free_adjacent_point, [])

        return True, directions_to_zip
    return False, []


def turn_corner_direction_update(
    coords: tuple[int, int], direction: int, board: dict[tuple[int, int], str]
) -> int:
    for i in [(direction + 1) % 4, (direction - 1) % 4]:
        next_coord = coords[0] + DIRECTIONS_MAP[i][0], coords[1] + DIRECTIONS_MAP[i][1]
        if next_coord in board:
            return i

    raise Exception(0)


def get_cube_position_direction_mapping(
    board: dict[tuple[int, int], str]
) -> dict[tuple[tuple[int, int], int], tuple[tuple[int, int], int]]:
    mapping = {}
    for coord in board:
        is_inner_coord, directions_to_zip = check_if_inner_corner(coord, board)
        if is_inner_coord:
            direction_anticlock, direction_clock = directions_to_zip
            direction_anticlock_prev, direction_clock_prev = directions_to_zip
            delta_a, delta_b = (
                DIRECTIONS_MAP[direction_anticlock],
                DIRECTIONS_MAP[direction_clock],
            )
            pointer_a, pointer_b = coord, coord

            while (
                direction_anticlock_prev == direction_anticlock
                or direction_clock_prev == direction_clock
            ):
                direction_anticlock_prev, direction_clock_prev = (
                    direction_anticlock,
                    direction_clock,
                )
                delta_a, delta_b = (
                    DIRECTIONS_MAP[direction_anticlock],
                    DIRECTIONS_MAP[direction_clock],
                )
                new_pointer_a = pointer_a[0] + delta_a[0], pointer_a[1] + delta_a[1]
                new_pointer_b = pointer_b[0] + delta_b[0], pointer_b[1] + delta_b[1]

                if new_pointer_a in board:
                    pointer_a = new_pointer_a
                else:
                    direction_anticlock = turn_corner_direction_update(
                        pointer_a, direction_anticlock, board
                    )

                if new_pointer_b in board:
                    pointer_b = new_pointer_b
                else:
                    direction_clock = turn_corner_direction_update(
                        pointer_b, direction_clock, board
                    )

                mapping[pointer_a, (direction_anticlock + 1) % 4] = (
                    pointer_b,
                    (direction_clock + 1) % 4,
                )
                mapping[pointer_b, (direction_clock - 1) % 4] = (
                    pointer_a,
                    (direction_anticlock - 1) % 4,
                )

    return mapping


def solve_part_2() -> int:
    board, instructions = parse_input_file()

    cube_position_direction_mapping = get_cube_position_direction_mapping(board)

    direction = 0
    position = (min([x for x, y in board if y == 0 and board[(x, y)] == "."]), 0)

    for instruction in instructions:
        if isinstance(instruction, int):
            for _ in range(instruction):
                new_position, new_direction = get_new_position_wrap_around_cube(
                    *position, direction, board, cube_position_direction_mapping
                )
                new_x, new_y = new_position
                if board.get((new_x, new_y)) == ".":
                    position, direction = (new_x, new_y), new_direction
                elif board.get((new_x, new_y)) == "#":
                    break

        else:
            match instruction:
                case "R":
                    direction = (direction + 1) % 4
                case "L":
                    direction = (direction - 1) % 4
                case _:
                    raise Exception(f"Invalid instruction in input: {instruction}")

    position_x, position_y = position
    return (1000 * (position_y + 1)) + (4 * (position_x + 1)) + direction


print("Day 22:")
print("Part 1 Solution:  ", solve_part_1())
print("Part 2 Solution:  ", solve_part_2())
