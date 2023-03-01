from os import path

input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
lines = input_file.read().strip().splitlines()


class CPU:
    def __init__(self, instructions):
        self.instructions = instructions
        self.X = 1
        self.cycle_number = 1
        self.signal_strength = 0
        self.pixel_output = ""
        self.cycles_to_calculate_signal_strength = list(range(20, 260, 40))

    def update_pixel_output_for_cycle(self, cycle_number: int):
        if abs(((cycle_number - 1) % 40) - self.X) <= 1:
            self.pixel_output += "#"
        else:
            self.pixel_output += "."

    def update_signal_strength(self, cycle_number: int):
        if cycle_number in self.cycles_to_calculate_signal_strength:
            self.signal_strength += cycle_number * self.X

    def run_instructions(self):
        for line in self.instructions:
            self.update_signal_strength(self.cycle_number)

            if (self.cycle_number - 1) % 40 == 0:
                self.pixel_output += "\n"

            if line[:4] == "noop":
                self.update_pixel_output_for_cycle(self.cycle_number)
                self.cycle_number += 1

            elif line[:4] == "addx":
                self.update_pixel_output_for_cycle(self.cycle_number)
                _, value = line.split()
                self.update_signal_strength(self.cycle_number + 1)

                if self.cycle_number % 40 == 0:
                    self.pixel_output += "\n"

                self.update_pixel_output_for_cycle(self.cycle_number + 1)

                self.cycle_number += 2
                self.X += int(value)

            else:
                raise Exception(f"Unknown instruction: {line}")


cpu = CPU(lines)
cpu.run_instructions()


print("Day 10:")
print("Part 1 Solution:  ", cpu.signal_strength)
print("Part 2 Solution:  ", cpu.pixel_output)
