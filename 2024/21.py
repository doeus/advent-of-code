from dataclasses import dataclass
from functools import cache
from itertools import pairwise


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def __add__(self, other: "Position") -> "Position":
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Position") -> "Position":
        return Position(self.x - other.x, self.y - other.y)


NUMERICAL_KEYPAD = ("789", "456", "123", " 0A")
DIRECTIONAL_KEYPAD = (" ^A", "<v>")


@cache
def find_key_position(keypad: tuple[str, ...], key: str) -> Position:
    for y in range(len(keypad)):
        for x in range(len(keypad[0])):
            if keypad[y][x] == key:
                return Position(x, y)

    raise ValueError()


@cache
def is_valid_path(keypad: tuple[str, ...], path: str, position: Position) -> bool:
    invalid_position = find_key_position(keypad, " ")

    for direction in path:
        match direction:
            case "<":
                position = Position(position.x - 1, position.y)
            case ">":
                position = Position(position.x + 1, position.y)
            case "^":
                position = Position(position.x, position.y - 1)
            case "v":
                position = Position(position.x, position.y + 1)

        if position == invalid_position:
            return False

    return True


@cache
def find_paths(keypad: tuple[str, ...], current_key: str, next_key: str) -> list[str]:
    current_position = find_key_position(keypad, current_key)
    next_position = find_key_position(keypad, next_key)
    difference = next_position - current_position

    horizontal_symbol = ">" if difference.x > 0 else "<"
    vertical_symbol = "v" if difference.y > 0 else "^"

    paths = [
        horizontal_symbol * abs(difference.x) + vertical_symbol * abs(difference.y),
        vertical_symbol * abs(difference.y) + horizontal_symbol * abs(difference.x),
    ]

    return [path for path in paths if is_valid_path(keypad, path, current_position)]


@cache
def count_moves(code: str, dept: int, max_dept: int) -> int:
    if dept == max_dept + 1:
        return len(code)

    keypad = NUMERICAL_KEYPAD if dept == 0 else DIRECTIONAL_KEYPAD

    return sum(
        min(count_moves(path + "A", dept + 1, max_dept) for path in find_paths(keypad, current_key, next_key))
        for current_key, next_key in pairwise("A" + code)
    )


with open("input.txt", encoding="utf-8") as file:
    codes = list(map(str.strip, file.readlines()))

# Part 1.
print(sum(int(code[:3]) * count_moves(code, 0, 2) for code in codes))

# Part 2.
print(sum(int(code[:3]) * count_moves(code, 0, 25) for code in codes))
