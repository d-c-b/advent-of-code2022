from os import path
import re


def parse_input_file() -> dict[str, int | str]:
    input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
    split_input_lines = [
        line.split(": ") for line in input_file.read().strip().splitlines()
    ]
    return {
        monkey_name: int(yell) if yell.isdigit() else yell
        for monkey_name, yell in split_input_lines
    }


def calculate_expression(val_a: int, operator: str, val_b: int) -> int:
    match operator:
        case "+":
            return val_a + val_b
        case "-":
            return val_a - val_b
        case "*":
            return val_a * val_b
        case "/":
            return val_a // val_b
        case _:
            raise Exception("Invalid operator")


def get_monkey_number(
    input_dict: dict[str, int | str | None], monkey_name: str
) -> int | None:
    yell_value = input_dict.get(monkey_name)
    if yell_value is None:
        return None

    if isinstance(yell_value, int):
        return yell_value

    if isinstance(yell_value, str):
        if not re.match(r"[a-z]+ [\+\-\*\/] [a-z]+", yell_value):
            raise Exception(f"Invalid input: {yell_value}")
        yell_value = yell_value.replace(" ", "")
        a_monkey_name, operator, b_monkey_name = re.split(r"([\+\-\*\/])", yell_value)

        a_value = get_monkey_number(input_dict, a_monkey_name)
        if a_value is None:
            return None

        b_value = get_monkey_number(input_dict, b_monkey_name)
        if b_value is None:
            return None

        return calculate_expression(a_value, operator, b_value)

    else:
        raise Exception(
            f"Unexpected value found for monkey {monkey_name} in input: {yell_value}"
        )


def calculate_inverse(val_a: int, operator: str, val_b: int, right_null: bool) -> int:
    match operator:
        case "+":
            return val_a - val_b
        case "-":
            if not right_null:
                return val_a + val_b
            else:
                return val_b - val_a
        case "*":
            return val_a // val_b
        case "/":
            if not right_null:
                return val_a * val_b
            else:
                return val_b // val_a
        case _:
            raise Exception("Invalid operator")


def solve_part_1():
    input_dict = parse_input_file()
    return get_monkey_number(input_dict, "root")


def find_unknown_value_in_input(
    monkey_name: str, eq_value: int, input_dict: dict[str, int | str | None]
) -> int | None:
    if monkey_name == "humn":
        return eq_value

    monkey_val = input_dict.get(monkey_name)

    if isinstance(monkey_val, str):
        monkey_a, operator, monkey_b = re.split(r" ([\+\-\*\/]) ", monkey_val)
        a_val = get_monkey_number(input_dict, monkey_a)
        b_val = get_monkey_number(input_dict, monkey_b)

        if a_val is None:
            assert b_val is not None
            eq_val = calculate_inverse(eq_value, operator, b_val, False)
            return find_unknown_value_in_input(monkey_a, eq_val, input_dict)

        elif b_val is None:
            eq_val = calculate_inverse(eq_value, operator, a_val, True)
            return find_unknown_value_in_input(monkey_b, eq_val, input_dict)

        else:
            raise Exception("No unknown value")

    return monkey_val


def solve_part_2():
    input_dict = parse_input_file()
    input_dict["humn"] = None
    input_dict["root"] = re.sub(r"[\+\-\*\/]", "-", input_dict.get("root"))

    return find_unknown_value_in_input("root", 0, input_dict)


print("Day 21:")
print("Part 1 Solution:  ", solve_part_1())
print("Part 2 Solution:  ", solve_part_2())
