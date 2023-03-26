from os import path
from collections import deque

input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
input = input_file.read().splitlines()


class HeightMap:
    def __init__(self, input_grid: list[list[str]]):
        self.start_coords = self.find_coords(input_grid, "S")
        self.end_coords = self.find_coords(input_grid, "E")
        input_grid[self.start_coords[1]][self.start_coords[0]] = "a"
        input_grid[self.end_coords[1]][self.end_coords[0]] = "z"
        self.grid = input_grid
        self.shortest_path_grid = [
            [float("inf") for _ in range(len(self.grid[0]))]
            for _ in range(len(self.grid))
        ]

    def find_coords(self, grid: list[list[str]], char_to_find: str) -> tuple[int, int]:
        for y, row in enumerate(grid):
            for x, char in enumerate(row):
                if char == char_to_find:
                    return (x, y)
        raise Exception(f"Character '{char_to_find}' not found in input file")

    def calculate_shortest_paths(self) -> list[list[int | float]]:
        self.shortest_path_grid[self.end_coords[1]][self.end_coords[0]] = 0
        to_visit = deque([self.end_coords])
        visited = set()
        while to_visit:
            current_pos = to_visit.popleft()
            neighbours = [
                (current_pos[0] + dx, current_pos[1] + dy)
                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]
                if current_pos[0] + dx in range(len(self.grid[0]))
                and current_pos[1] + dy in range(len(self.grid))
            ]
            for neighbour in neighbours:
                if (
                    ord(self.grid[current_pos[1]][current_pos[0]])
                    - ord(self.grid[neighbour[1]][neighbour[0]])
                    <= 1
                    and neighbour not in visited
                ):
                    if (
                        self.shortest_path_grid[neighbour[1]][neighbour[0]]
                        > self.shortest_path_grid[current_pos[1]][current_pos[0]] + 1
                    ):
                        self.shortest_path_grid[neighbour[1]][neighbour[0]] = (
                            self.shortest_path_grid[current_pos[1]][current_pos[0]] + 1
                        )
                    visited.add(neighbour)
                    to_visit.append(neighbour)

        return self.shortest_path_grid

    def possible_start_positions(self) -> list[tuple[int, int]]:
        start_positions = []
        for y, row in enumerate(self.grid):
            for x, char in enumerate(row):
                if char == "a":
                    start_positions.append((x, y))
        return start_positions


input_grid = [[i for i in row] for row in input]
hill_height_map = HeightMap(input_grid)

shortest_paths = hill_height_map.calculate_shortest_paths()

print("Day 12:")
print(
    "Part 1 Solution:  ",
    shortest_paths[hill_height_map.start_coords[1]][hill_height_map.start_coords[0]],
)
print(
    "Part 2 Solution:  ",
    min(
        [shortest_paths[s[1]][s[0]] for s in hill_height_map.possible_start_positions()]
    ),
)
