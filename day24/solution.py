from os import path


BLIZZARD_MOVEMENTS = {
    "^": (0, -1),
    "v": (0, 1),
    "<": (-1, 0),
    ">": (1, 0),
}


class ValleyGrid:
    def __init__(
        self,
        open_spaces: set[tuple[int, int]],
        blizzard_positions: dict[str, set[tuple[int, int]]],
    ):
        self.open_spaces = open_spaces
        self.blizzard_positions = blizzard_positions
        self.min_y = min([y for (_, y) in open_spaces])
        self.max_y = max([y for (_, y) in open_spaces])
        self.min_x = min([x for (x, _) in open_spaces])
        self.max_x = max([x for (x, _) in open_spaces])
        self.height = self.max_y - self.min_y + 1
        self.width = self.max_x - self.min_x + 1

    def find_shortest_time_between_two_points(
        self, start: tuple[int, int], end: tuple[int, int], start_time: int
    ) -> int:
        possible_positions = set([start])
        time = start_time
        while end not in possible_positions:
            time += 1
            blizzard_positions = set()
            for direction in BLIZZARD_MOVEMENTS.keys():
                dx, dy = BLIZZARD_MOVEMENTS[direction]
                blizzard_positions.update(
                    [
                        (
                            (x - self.min_x + dx * time) % self.width + self.min_x,
                            (
                                (y - self.min_y - 1 + dy * time) % (self.height - 2)
                                + self.min_y
                                + 1
                            ),
                        )
                        for x, y in self.blizzard_positions[direction]
                    ]
                )

            new_positions = (
                set(
                    [
                        (x + dx, y + dy)
                        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]
                        for x, y in possible_positions
                    ]
                ).intersection(self.open_spaces)
                | possible_positions
            )

            possible_positions = new_positions - blizzard_positions

        return time


def parse_input_file() -> tuple[set[tuple[int, int]], dict[str, set[tuple[int, int]]]]:
    input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
    lines = input_file.read().strip().splitlines()

    open_spaces = set()
    blizzards: dict[str, set[tuple[int, int]]] = {
        "^": set(),
        "v": set(),
        "<": set(),
        ">": set(),
    }
    for j, line in enumerate(lines):
        for i, char in enumerate(line):
            if char == "#":
                continue
            open_spaces.add((i, j))
            if char != ".":
                blizzards[char].add((i, j))

    return open_spaces, blizzards


def solve_part_1():
    open_spaces, blizzards = parse_input_file()

    valley = ValleyGrid(open_spaces, blizzards)
    start = (1, 0)
    end = (valley.width, valley.height - 1)

    shortest_time = valley.find_shortest_time_between_two_points(start, end, 0)
    return shortest_time


def solve_part_2():
    open_spaces, blizzards = parse_input_file()
    valley = ValleyGrid(open_spaces, blizzards)
    start = (1, 0)
    end = (valley.width, valley.height - 1)

    paths = [(start, end), (end, start), (start, end)]

    total_time = 0
    for start, end in paths:
        total_time = valley.find_shortest_time_between_two_points(
            start, end, total_time
        )

    return total_time


print("Day 24:")
print("Part 1 Solution:  ", solve_part_1())
print("Part 2 Solution:  ", solve_part_2())
