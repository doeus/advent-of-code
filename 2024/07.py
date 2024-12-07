def is_possible(target: int, current: int, rest: tuple[int, ...]) -> bool:
    if len(rest) == 0:
        return current == target
    return is_possible(target, current + rest[0], rest[1:]) or is_possible(target, current * rest[0], rest[1:])


def is_possible_with_concatenation(target: int, current: int, rest: tuple[int, ...]) -> bool:
    if len(rest) == 0:
        return current == target
    return (
        is_possible_with_concatenation(target, current + rest[0], rest[1:])
        or is_possible_with_concatenation(target, current * rest[0], rest[1:])
        or is_possible_with_concatenation(target, int(str(current) + str(rest[0])), rest[1:])
    )


with open("input.txt", encoding="utf-8") as file:
    lines = file.readlines()

tests = [(int(target), tuple(map(int, numbers.split()))) for target, numbers in (line.split(":") for line in lines)]

# Part 1.
print(sum(target for target, numbers in tests if is_possible(target, numbers[0], numbers[1:])))

# Part 2.
print(sum(target for target, numbers in tests if is_possible_with_concatenation(target, numbers[0], numbers[1:])))
