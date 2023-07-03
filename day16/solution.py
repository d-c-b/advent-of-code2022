from os import path
import re
from collections import deque


def parse_input_file() -> tuple[dict[str, list[str]], dict[str, int]]:
    input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
    lines = input_file.read().strip().splitlines()
    valve_paths = {}
    valve_rates = {}
    for line in lines:
        valves = re.findall(r"[A-Z]{2}", line)
        valve = str(valves[0])
        rate_in_line = re.search(r"\d+", line)
        if not rate_in_line:
            raise Exception(f"No rate found in input line for valve {valve}")
        rate = int(rate_in_line.group())
        valve_rates[valve] = rate
        valve_paths[valve] = [str(valve) for valve in valves[1:]]

    return valve_paths, valve_rates


def shortest_paths(
    valve_paths: dict[str, list[str]]
) -> dict[str, dict[str, int | float]]:
    valve_shortest_paths = {}

    for valve, directly_linked in valve_paths.items():
        shortest_paths_for_valve = {
            v: float("inf")
            for v in valve_paths
            if v not in directly_linked and v != valve
        }
        shortest_paths_for_valve[valve] = 0
        for dl in directly_linked:
            shortest_paths_for_valve[dl] = 1

        valve_shortest_paths[valve] = shortest_paths_for_valve

    for k in valve_paths:
        for i in valve_paths:
            for j in valve_paths:
                if (
                    valve_shortest_paths[i][j]
                    > valve_shortest_paths[i][k] + valve_shortest_paths[k][j]
                ):
                    valve_shortest_paths[i][j] = (
                        valve_shortest_paths[i][k] + valve_shortest_paths[k][j]
                    )

    return valve_shortest_paths


def solve(total_time: int) -> dict[tuple[str, ...], int]:
    valve_paths, valve_rates = parse_input_file()
    valve_shortest_paths = shortest_paths(valve_paths)
    non_zero_valves = [valve for valve, rate in valve_rates.items() if rate > 0]

    initial_state: tuple[str, set[str], int, int] = ("AA", set(), 0, total_time)

    rates = []
    max_rates_for_opened_set: dict[tuple[str, ...], int] = {}
    states = deque([initial_state])

    while states:
        current_valve, opened_valves, flow, time_left = states.popleft()
        rates.append(flow)

        opened_key = tuple(opened_valves)
        max_rates_for_opened_set[opened_key] = max(
            flow, max_rates_for_opened_set.get(opened_key, 0)
        )

        if valve_rates[current_valve] > 0 and current_valve not in opened_valves:
            flow_from_current = (time_left - 1) * valve_rates[current_valve]
            states.append(
                (
                    current_valve,
                    set([*opened_valves, current_valve]),
                    flow + flow_from_current,
                    time_left - 1,
                )
            )
            continue

        for next_valve in non_zero_valves:
            if next_valve not in opened_valves:
                dist = int(valve_shortest_paths[current_valve][next_valve])
                if time_left - dist > 1:
                    states.append((next_valve, opened_valves, flow, time_left - dist))

    return max_rates_for_opened_set


def solve_part_1(total_time: int) -> int:
    max_rates = solve(total_time)
    return max(max_rates.values())


def solve_part_2(total_time: int) -> int:
    rates_for_opened_set = solve(total_time)

    unique_set_combinations = []
    for key1 in rates_for_opened_set.keys():
        for key2 in rates_for_opened_set.keys():
            if not set(key1) & set(key2):
                unique_set_combinations.append((key1, key2))

    return max(
        [
            rates_for_opened_set[key1] + rates_for_opened_set[key2]
            for key1, key2 in unique_set_combinations
        ]
    )


print("Day 16:")
print("Part 1 Solution:  ", solve_part_1(30))
print("Part 2 Solution:  ", solve_part_2(26))
