from os import path
import re
from collections import deque, namedtuple


def parse_input_file() -> dict[int, list[int]]:
    input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
    blueprints = {}
    for line in input_file.read().strip().splitlines():
        if not re.match(
            r"Blueprint \d+\: Each ore robot costs \d+ ore. Each clay robot costs \d+ ore. Each obsidian robot costs \d+ ore and \d+ clay. Each geode robot costs \d+ ore and \d+ obsidian.",
            line,
        ):
            raise Exception(f"Unexpected input line: {line}")

        id, *rest = [int(n) for n in re.findall(r"\d+", line)]
        blueprints[id] = rest
    return blueprints


def solve_max_geodes_opened(
    time,
    ore_robot_cost,
    clay_robot_cost,
    obs_robot_cost_ore,
    obs_robot_cost_clay,
    geode_robot_cost_ore,
    geode_robot_cost_obs,
) -> int:

    max_geodes = 0
    State = namedtuple(
        "State",
        [
            "time",
            "n_ore_robot",
            "n_ore",
            "n_clay_robot",
            "n_clay",
            "n_obs_robot",
            "n_obs",
            "n_geode_robot",
            "n_geodes",
        ],
    )
    init = State(
        time=time,
        n_ore_robot=1,
        n_ore=0,
        n_clay_robot=0,
        n_clay=0,
        n_obs_robot=0,
        n_obs=0,
        n_geode_robot=0,
        n_geodes=0,
    )

    states = deque([init])

    max_ore_robots = max(
        ore_robot_cost, clay_robot_cost, obs_robot_cost_ore, geode_robot_cost_ore
    )
    max_clay_robots = obs_robot_cost_clay
    max_obsidian_robots = geode_robot_cost_obs
    seen_states = set()

    while states:

        state = states.popleft()
        max_geodes = max(max_geodes, state.n_geodes)

        if state.time == 0:
            continue

        if state in seen_states:
            continue

        seen_states.add(state)

        # Check if best case of creating new geode robot every second until the end
        # will still be less than current max, if so can skip all states from this path
        if (
            state.n_geodes
            + (state.n_geode_robot * state.time)
            + ((state.time * (state.time - 1)) / 2)
            < max_geodes
        ):
            continue

        if (state.n_ore >= geode_robot_cost_ore) and (
            state.n_obs >= geode_robot_cost_obs
        ):
            states.append(
                State(
                    time=state.time - 1,
                    n_ore_robot=state.n_ore_robot,
                    n_ore=state.n_ore + state.n_ore_robot - geode_robot_cost_ore,
                    n_clay_robot=state.n_clay_robot,
                    n_clay=state.n_clay + state.n_clay_robot,
                    n_obs_robot=state.n_obs_robot,
                    n_obs=state.n_obs + state.n_obs_robot - geode_robot_cost_obs,
                    n_geode_robot=state.n_geode_robot + 1,
                    n_geodes=state.n_geodes + state.n_geode_robot,
                )
            )
            continue

        if (
            state.n_ore >= obs_robot_cost_ore
            and state.n_clay >= obs_robot_cost_clay
            and state.n_obs_robot < max_obsidian_robots
        ):
            states.append(
                State(
                    time=state.time - 1,
                    n_ore_robot=state.n_ore_robot,
                    n_ore=state.n_ore + state.n_ore_robot - obs_robot_cost_ore,
                    n_clay_robot=state.n_clay_robot,
                    n_clay=state.n_clay + state.n_clay_robot - obs_robot_cost_clay,
                    n_obs_robot=state.n_obs_robot + 1,
                    n_obs=state.n_obs + state.n_obs_robot,
                    n_geode_robot=state.n_geode_robot,
                    n_geodes=state.n_geodes + state.n_geode_robot,
                )
            )

        if state.n_ore >= clay_robot_cost and state.n_clay_robot < max_clay_robots:
            states.append(
                State(
                    time=state.time - 1,
                    n_ore_robot=state.n_ore_robot,
                    n_ore=state.n_ore + state.n_ore_robot - clay_robot_cost,
                    n_clay_robot=state.n_clay_robot + 1,
                    n_clay=state.n_clay + state.n_clay_robot,
                    n_obs_robot=state.n_obs_robot,
                    n_obs=state.n_obs + state.n_obs_robot,
                    n_geode_robot=state.n_geode_robot,
                    n_geodes=state.n_geodes + state.n_geode_robot,
                )
            )

        if state.n_ore >= ore_robot_cost and state.n_ore_robot < max_ore_robots:
            states.append(
                State(
                    time=state.time - 1,
                    n_ore_robot=state.n_ore_robot + 1,
                    n_ore=state.n_ore + state.n_ore_robot - ore_robot_cost,
                    n_clay_robot=state.n_clay_robot,
                    n_clay=state.n_clay + state.n_clay_robot,
                    n_obs_robot=state.n_obs_robot,
                    n_obs=state.n_obs + state.n_obs_robot,
                    n_geode_robot=state.n_geode_robot,
                    n_geodes=state.n_geodes + state.n_geode_robot,
                )
            )

        states.append(
            State(
                time=state.time - 1,
                n_ore_robot=state.n_ore_robot,
                n_ore=state.n_ore + state.n_ore_robot,
                n_clay_robot=state.n_clay_robot,
                n_clay=state.n_clay + state.n_clay_robot,
                n_obs_robot=state.n_obs_robot,
                n_obs=state.n_obs + state.n_obs_robot,
                n_geode_robot=state.n_geode_robot,
                n_geodes=state.n_geodes + state.n_geode_robot,
            )
        )

    return max_geodes


def solve_part_1(time: int) -> int:
    blueprints = parse_input_file()
    score = 0
    for id, costs in blueprints.items():
        max_g = solve_max_geodes_opened(
            time,
            *costs,
        )

        score += id * max_g
    return score


def solve_part_2(time: int) -> int:
    blueprints = parse_input_file()
    score = 1
    for costs in list(blueprints.values())[:3]:
        max_g = solve_max_geodes_opened(
            time,
            *costs,
        )
        score *= max_g
    return score


print("Day 19:")
print("Part 1 Solution:  ", solve_part_1(24))
print("Part 2 Solution:  ", solve_part_2(32))
