from os import path


ROCK_SHAPES = [
    ((0, 0), (1, 0), (2, 0), (3, 0)),
    ((1, 0), (0, 1), (1, 1), (2, 1), (1, 2)),
    ((0, 0), (1, 0), (2, 0), (2, 1), (2, 2)),
    ((0, 0), (0, 1), (0, 2), (0, 3)),
    ((0, 0), (1, 0), (0, 1), (1, 1)),
]

ROCK_START_X_OFFSET = 2
ROCK_START_Y_OFFSET = 3


def parse_input_file() -> str:
    input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
    input = input_file.read().strip()

    return input


def solve(total_iterations: int) -> int:
    gas_jets = parse_input_file()
    tower = set((i, 0) for i in range(7))
    jet_i = 0

    check_for_cycles: dict[tuple[int, int], tuple[int, int]] = {}

    for rock_i in range(total_iterations):

        rock_type_index = rock_i % len(ROCK_SHAPES)

        height = max([y for _, y in tower])
        at_rest = False
        rock_position = [
            (x + ROCK_START_X_OFFSET, y + ROCK_START_Y_OFFSET + height + 1)
            for x, y in ROCK_SHAPES[rock_type_index]
        ]

        rock_index_jet_index_pair = (rock_type_index, jet_i % len(gas_jets))

        if rock_index_jet_index_pair in check_for_cycles:
            prev_rock_index, prev_height = check_for_cycles[rock_index_jet_index_pair]
            quotient, remainder = divmod(
                total_iterations - rock_i, rock_i - prev_rock_index
            )
            if remainder == 0:
                return height + (height - prev_height) * quotient

        else:
            check_for_cycles[rock_index_jet_index_pair] = rock_i, height

        while not at_rest:
            jet_index = jet_i % len(gas_jets)

            if gas_jets[jet_index] == ">":
                if all(
                    [x + 1 < 7 and (x + 1, y) not in tower for x, y in rock_position]
                ):
                    rock_position = [(x + 1, y) for x, y in rock_position]
            elif gas_jets[jet_index] == "<":
                if all(
                    [x - 1 >= 0 and (x - 1, y) not in tower for x, y in rock_position]
                ):
                    rock_position = [(x - 1, y) for x, y in rock_position]

            if any([(x, y - 1) in tower for x, y in rock_position]):
                tower.update(rock_position)
                at_rest = True

            else:
                rock_position = [(x, y - 1) for x, y in rock_position]

            jet_i += 1

    return max([y for _, y in tower])


print("Day 17:")
print("Part 1 Solution:  ", solve(2022))
print("Part 2 Solution:  ", solve(1000000000000))
