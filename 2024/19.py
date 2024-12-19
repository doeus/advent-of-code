from functools import cache


def is_possible(design: str) -> bool:
    if design in towels:
        return True

    for i in range(1, len(design)):
        if design[:i] in towels and is_possible(design[i:]):
            return True

    return False


@cache
def count_arrangements(design: str) -> int:
    count = 0

    if design in towels:
        count += 1

    for i in range(1, len(design)):
        if design[:i] in towels:
            count += count_arrangements(design[i:])

    return count


with open("input.txt", encoding="utf-8") as file:
    towel_input, design_input = file.read().split("\n\n")

towels = set(towel_input.split(", "))
designs = design_input.splitlines()

# Part 1.
print(sum(map(is_possible, designs)))

# Part 2.
print(sum(map(count_arrangements, designs)))
