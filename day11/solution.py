from os import path
import re
from typing import Callable, Dict
import math

input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
monkey_input = input_file.read().strip().split("\n\n")


class Monkey:
    def __init__(
        self,
        items: list[int],
        operation: Callable[[int], int],
        div_by_test: int,
        true_pass_to_monkey: int,
        false_pass_to_monkey: int,
    ):
        self.items = items
        self.operation = operation
        self.div_by_test = div_by_test
        self.true_pass_to_monkey = true_pass_to_monkey
        self.false_pass_to_monkey = false_pass_to_monkey
        self.inspected_items = 0


def parse_operation(op_string: str) -> Callable[[int], int]:
    expression = op_string.split("=")[1].split()
    operator = expression[1]
    second_operand = expression[2]

    match operator:
        case "+":
            if second_operand == "old":
                return lambda x: x + x
            else:
                return lambda x: x + int(second_operand)

        case "*":
            if second_operand == "old":
                return lambda x: x * x
            else:
                return lambda x: x * int(second_operand)
        case _:
            raise Exception("Invalid operator")


def parse_monkey_input_data(
    monkey_input: list[str],
) -> tuple[int, list[int], Callable[[int], int], int, int, int]:
    if not re.match(r"^Monkey \d:$", monkey_input[0]):
        raise Exception(f"Error in monkey input line: {monkey_input[0]}")

    if not re.match(r"^Starting items: \d+(, ?\d+)*$", monkey_input[1].strip()):
        raise Exception(f"Error in monkey input line: {monkey_input[1]}")

    if not re.match(
        r"^Operation: new = old (\+|\*) (old|\d+)$", monkey_input[2].strip()
    ):
        raise Exception(f"Error in monkey input line: {monkey_input[2]}")

    if not re.match(r"^Test: divisible by \d+$", monkey_input[3].strip()):
        raise Exception(f"Error in monkey input line: {monkey_input[3]}")

    if not re.match(r"^If true: throw to monkey \d+$", monkey_input[4].strip()):
        raise Exception(f"Error in monkey input line: {monkey_input[4]}")

    if not re.match(r"^If false: throw to monkey \d+$", monkey_input[5].strip()):
        raise Exception(f"Error in monkey input line: {monkey_input[5]}")

    monkey_id = int(monkey_input[0].strip(":").split()[1])
    starting_items = [int(x) for x in monkey_input[1].split(":")[1].split(",")]
    operation = parse_operation(monkey_input[2])
    div_by_test = int(monkey_input[3].split()[-1])
    true_pass_to_monkey = int(monkey_input[4].split()[-1])
    false_pass_to_monkey = int(monkey_input[5].split()[-1])

    return (
        monkey_id,
        starting_items,
        operation,
        div_by_test,
        true_pass_to_monkey,
        false_pass_to_monkey,
    )


def initialise_monkeys(monkeys_input: list[str]) -> Dict[int, Monkey]:
    monkeys = {}
    monkey_inputs = [m.splitlines() for m in monkeys_input]
    for monkey_input in monkey_inputs:
        (
            monkey_id,
            starting_items,
            operation,
            div_by_test,
            true_pass_to_monkey,
            false_pass_to_monkey,
        ) = parse_monkey_input_data(monkey_input)

        monkeys[monkey_id] = Monkey(
            items=starting_items,
            operation=operation,
            div_by_test=div_by_test,
            true_pass_to_monkey=true_pass_to_monkey,
            false_pass_to_monkey=false_pass_to_monkey,
        )

    return monkeys


def solve_monkeys(number_of_rounds: int, worry_reduction_div_by_3: bool = False) -> int:
    monkeys = initialise_monkeys(monkey_input)
    lcm_divisor = math.prod([m.div_by_test for m in monkeys.values()])
    for _ in range(number_of_rounds):
        for monkey in monkeys.values():
            for item in monkey.items:
                new_value = monkey.operation(item)
                monkey.inspected_items += 1
                new_value = (
                    new_value // 3
                    if worry_reduction_div_by_3
                    else new_value % lcm_divisor
                )
                if new_value % monkey.div_by_test == 0:
                    monkeys[monkey.true_pass_to_monkey].items.append(new_value)
                else:
                    monkeys[monkey.false_pass_to_monkey].items.append(new_value)
            monkey.items = []

    sorted_inspected_item_counts = sorted(
        [m.inspected_items for m in monkeys.values()], reverse=True
    )
    return math.prod(sorted_inspected_item_counts[0:2])


print("Day 11:")
print("Part 1 Solution:  ", solve_monkeys(20, True))
print("Part 2 Solution:  ", solve_monkeys(10000))
