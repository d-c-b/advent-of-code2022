from os import path
import math

input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
lines = input_file.read().strip().splitlines()


class Rope:
    def __init__(self, number_of_knots: int):
        self.number_of_knots = number_of_knots
        self.positions = [[0, 0] for _ in range(number_of_knots)]
        self.tail_visited_positions = set([(0, 0)])

    def move_head_position(self, direction: str):
        match direction:
            case "U":
                self.positions[0][1] += 1
            case "D":
                self.positions[0][1] -= 1
            case "L":
                self.positions[0][0] -= 1
            case "R":
                self.positions[0][0] += 1
            case _:
                raise Exception(f"Unknown direction: {direction}")

        for i in range(1, self.number_of_knots):
            x_diff = self.positions[i - 1][0] - self.positions[i][0]
            y_diff = self.positions[i - 1][1] - self.positions[i][1]

            if abs(x_diff) <= 1 and abs(y_diff) <= 1:
                continue

            if y_diff != 0:
                self.positions[i][1] += int(math.copysign(1, y_diff))
            if x_diff != 0:
                self.positions[i][0] += int(math.copysign(1, x_diff))

        self.tail_visited_positions.add((self.positions[-1][0], self.positions[-1][1]))


rope_2_knots = Rope(2)
rope_10_knots = Rope(10)

for line in lines:
    direction, distance = line.split()
    for _ in range(int(distance)):
        rope_2_knots.move_head_position(direction)
        rope_10_knots.move_head_position(direction)


print("Day 09:")
print("Part 1 Solution:  ", len(rope_2_knots.tail_visited_positions))
print("Part 2 Solution:  ", len(rope_10_knots.tail_visited_positions))
