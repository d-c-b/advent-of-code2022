from os import path

input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
lines = input_file.read().strip().splitlines()


forest = [[int(c) for c in line] for line in lines]

WIDTH = len(forest[0])
HEIGHT = len(forest)


def is_visible(grid: list[list[int]], y: int, x: int) -> bool:
    shorter_from_left = [1 if grid[y][i] < grid[y][x] else 0 for i in range(0, x)]
    shorter_from_right = [
        1 if grid[y][i] < grid[y][x] else 0 for i in range(x + 1, WIDTH)
    ]

    shorter_from_top = [1 if grid[j][x] < grid[y][x] else 0 for j in range(0, y)]
    shorter_from_bottom = [
        1 if grid[j][x] < grid[y][x] else 0 for j in range(y + 1, HEIGHT)
    ]

    return any(
        [
            all(shorter_from_left),
            all(shorter_from_right),
            all(shorter_from_top),
            all(shorter_from_bottom),
        ]
    )


def count_visible_trees(grid: list[list[int]]) -> int:
    count = 0
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if is_visible(grid, y, x):
                count += 1
    return count


def calculate_scenic_score(grid: list[list[int]], y: int, x: int) -> int:
    trees_up = [grid[j][x] for j in range(y - 1, -1, -1)]
    trees_down = [grid[j][x] for j in range(y + 1, HEIGHT)]
    trees_left = [grid[y][i] for i in range(x - 1, -1, -1)]
    trees_right = [grid[y][i] for i in range(x + 1, WIDTH)]
    scenic_score = 1
    for tree_row in [trees_up, trees_right, trees_down, trees_left]:
        try:
            dist = next(
                index + 1 for index, value in enumerate(tree_row) if value >= grid[y][x]
            )
            scenic_score *= dist
        except StopIteration:
            scenic_score *= len(tree_row)

    return scenic_score


def calculate_max_scenic_score(grid: list[list[int]]) -> int:
    max_scenic_score = 0
    for y in range(HEIGHT):
        for x in range(WIDTH):
            scenic_score_value = calculate_scenic_score(grid, y, x)
            if scenic_score_value > max_scenic_score:
                max_scenic_score = scenic_score_value
    return max_scenic_score


print("Day 08:")
print("Part 1 Solution:  ", count_visible_trees(forest))
print("Part 2 Solution:  ", calculate_max_scenic_score(forest))
