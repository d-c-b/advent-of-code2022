from os import path

input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
lines = input_file.read().strip().splitlines()


def find_shared_character_across_compartments(line: str) -> str:
    string1, string2 = line[: len(line) // 2], line[len(line) // 2 :]
    shared_characters = [x for x in set(string1) if x in set(string2)]
    if len(shared_characters) == 0:
        raise Exception(f"No shared characters in compartments of {line}")
    if len(shared_characters) > 1:
        raise Exception(
            f"More than 1 shared character found in compartments of {line}: {shared_characters}"
        )
    return shared_characters[0]


def get_priority_score(character: str) -> int:
    if character.isupper():
        return ord(character) - ord("A") + 27

    elif character.islower():
        return ord(character) - ord("a") + 1
    else:
        raise Exception(f"Invalid character: {character}")


priorities = [
    get_priority_score(find_shared_character_across_compartments(line))
    for line in lines
]


def find_shared_characters_across_3_lines(line1: str, line2: str, line3: str) -> str:
    shared_characters = list(set(line1) & set(line2) & set(line3))
    if len(shared_characters) == 0:
        raise Exception(
            f"No shared characters in lines of {line1} , {line2} and {line3}"
        )
    if len(shared_characters) > 1:
        raise Exception(
            f"More than 1 shared character found in  {line1} , {line2} and {line3}:  {shared_characters}"
        )
    return shared_characters[0]


priorities2 = [
    get_priority_score(find_shared_characters_across_3_lines(a, b, c))
    for a, b, c in zip(lines[::3], lines[1::3], lines[2::3])
]


print("Day 03:")
print("Part 1 Solution:  ", sum(priorities))
print("Part 2 Solution:  ", sum(priorities2))
