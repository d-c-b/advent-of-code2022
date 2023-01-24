from os import path
from enum import Enum

input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
raw_input = input_file.read().strip()


class MyPlayValues(Enum):
    X = 0
    Y = 1
    Z = 2


class OpponentPlayValues(Enum):
    A = 0
    B = 1
    C = 2


def calculate_score_for_round_specified_play(opponent_play_value, my_play_value):
    mod_val = (my_play_value - opponent_play_value) % 3
    if mod_val == 0:
        outcome_score = 3
    if mod_val == 1:
        outcome_score = 6
    if mod_val == 2:
        outcome_score = 0
    bonus_score = my_play_value + 1
    return outcome_score + bonus_score


def calculate_score_for_round_specified_outcome(opponent_play_value, expected_outcome):
    my_play_value = (opponent_play_value + (expected_outcome + 2) % 3) % 3
    outcome_score = 3 * expected_outcome
    return outcome_score + my_play_value + 1


total_score_1 = 0
total_score_2 = 0

for i, line in enumerate(raw_input.splitlines()):
    opponent_play, my_play = line.split()
    if opponent_play not in [v.name for v in OpponentPlayValues] or my_play not in [
        v.name for v in MyPlayValues
    ]:
        raise Exception("Unexpected input value")

    opponent_play_value = OpponentPlayValues[opponent_play].value
    my_play_value = MyPlayValues[my_play].value

    round_score_1 = calculate_score_for_round_specified_play(
        opponent_play_value, my_play_value
    )
    total_score_1 += round_score_1
    round_score_2 = calculate_score_for_round_specified_outcome(
        opponent_play_value, my_play_value
    )
    total_score_2 += round_score_2


print("Day 02:")
print("Part 1 Solution:  ", total_score_1)
print("Part 2 Solution:  ", total_score_2)
