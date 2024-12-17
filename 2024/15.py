from collections import deque
from dataclasses import dataclass


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def __add__(self, other: "Position") -> "Position":
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Position") -> "Position":
        return Position(self.x - other.x, self.y - other.y)


DIRECTIONS = {"^": Position(0, -1), ">": Position(1, 0), "v": Position(0, 1), "<": Position(-1, 0)}


def find_robot() -> Position | None:
    for y in range(width):
        for x in range(height):
            if warehouse[y][x] == "@":
                return Position(x, y)

    return None


def move(position: Position, direction: Position) -> bool:
    current = position

    while warehouse[current.y][current.x] not in {".", "#"}:
        current += direction

    if warehouse[current.y][current.x] == "#":
        return False

    while current != position:
        previous = current - direction
        warehouse[current.y][current.x] = warehouse[previous.y][previous.x]
        warehouse[previous.y][previous.x] = "."
        current = previous

    return True


def move_wide(position: Position, direction: Position) -> bool:
    if direction in {DIRECTIONS["<"], DIRECTIONS[">"]}:
        return move(position, direction)

    search_queue = deque([position])
    visited_queue = deque()

    while len(search_queue):
        current = search_queue.popleft()
        visited_queue.append(current)

        next_position_a = current + direction
        next_position_b = next_position_a + (
            DIRECTIONS[">"] if warehouse[next_position_a.y][next_position_a.x] == "[" else DIRECTIONS["<"]
        )

        if warehouse[next_position_a.y][next_position_a.x] not in "[]":
            next_position_b = next_position_a

        if (
            warehouse[next_position_a.y][next_position_a.x] == "#"
            or warehouse[next_position_b.y][next_position_b.x] == "#"
        ):
            return False

        if (
            warehouse[next_position_a.y][next_position_a.x] != "."
            and next_position_a not in search_queue
            and next_position_a not in visited_queue
        ):
            search_queue.append(next_position_a)

        if (
            warehouse[next_position_b.y][next_position_b.x] != "."
            and next_position_b not in search_queue
            and next_position_b not in visited_queue
        ):
            search_queue.append(next_position_b)

    while len(visited_queue):
        current = visited_queue.pop()
        next_position = current + direction
        warehouse[next_position.y][next_position.x] = warehouse[current.y][current.x]
        warehouse[current.y][current.x] = "."

    return True


with open("input.txt", encoding="utf-8") as file:
    warehouse_input, movement_input = file.read().split("\n\n")

# Part 1.
warehouse = [list(line) for line in warehouse_input.splitlines()]
movements = movement_input.replace("\n", "")
width = len(warehouse[0])
height = len(warehouse)
robot = find_robot()

for movement in movements:
    if move(robot, DIRECTIONS[movement]):
        robot += DIRECTIONS[movement]

print(sum(100 * y + x for y in range(height) for x in range(width) if warehouse[y][x] == "O"))

# Part 2.
warehouse = [
    list(line.translate(str.maketrans({"#": "##", "O": "[]", ".": "..", "@": "@."})))
    for line in warehouse_input.splitlines()
]
width = len(warehouse[0])
height = len(warehouse)
robot = find_robot()

for movement in movements:
    if move_wide(robot, DIRECTIONS[movement]):
        robot += DIRECTIONS[movement]

print(sum(100 * y + x for y in range(height) for x in range(width) if warehouse[y][x] == "["))
