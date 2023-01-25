from os import path
import re

input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
input_string = input_file.read().rstrip()

crate_model, instructions = input_string.split("\n\n")


def parse_instructions(raw_instructions_string: str) -> list[list[int]]:
    instructions_list = [
        instruction for instruction in raw_instructions_string.split("\n")
    ]
    parsed = []
    for instruction in instructions_list:
        if not re.match(r"move \d+ from \d+ to \d+", instruction):
            raise Exception(f"Unexpected instruction input: {instruction}")
        parsed.append([int(x) for x in re.findall(r"\d+", instruction)])

    return parsed


class CrateStacks:
    def __init__(self):
        self.stacks = [[] for _ in range(9)]
        self.instructions = parse_instructions(instructions)
        self.parse_initial_stack()

    def parse_initial_stack(self):
        crate_rows = [crate_row for crate_row in crate_model.split("\n")][:-1]

        for crate_row in crate_rows:
            for i, crate_value in enumerate(crate_row[1::4]):
                if crate_value != " ":
                    self.stacks[i].append(crate_value)

    def move_crate_9001(self, source_stack, destination_stack, number):
        moved = self.stacks[source_stack - 1][:number]
        self.stacks[source_stack - 1] = self.stacks[source_stack - 1][number:]
        self.stacks[destination_stack - 1] = moved + self.stacks[destination_stack - 1]

    def move_crate(self, source_stack, destination_stack):
        moved = self.stacks[source_stack - 1].pop(0)
        self.stacks[destination_stack - 1].insert(0, moved)

    def run_instructions(self):
        for number, source, destination in self.instructions:
            [self.move_crate(source, destination) for _ in range(number)]

    def run_instructions_9001(self):
        for number, source, destination in self.instructions:
            self.move_crate_9001(source, destination, number)


stack_instance_9000 = CrateStacks()
stack_instance_9000.run_instructions()


stack_instance_9001 = CrateStacks()
stack_instance_9001.run_instructions_9001()

print("Day 05:")
print(
    "Part 1 Solution:  ",
    "".join(
        [
            stack_instance_9000.stacks[i][0]
            for i in range(len(stack_instance_9000.stacks))
        ]
    ),
)
print(
    "Part 2 Solution:  ",
    "".join(
        [
            stack_instance_9001.stacks[i][0]
            for i in range(len(stack_instance_9001.stacks))
        ]
    ),
)
