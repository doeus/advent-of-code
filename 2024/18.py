from dataclasses import dataclass, field
from queue import PriorityQueue


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def __add__(self, other: "Position") -> "Position":
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Position") -> "Position":
        return Position(self.x - other.x, self.y - other.y)

    def __str__(self) -> str:
        return f"{self.x},{self.y}"


@dataclass(order=True)
class PrioritizedPosition:
    priority: int
    position: Position = field(compare=False)


DIRECTIONS = (Position(0, -1), Position(1, 0), Position(0, 1), Position(-1, 0))
WIDTH = 71
HEIGHT = 71
START = Position(0, 0)
END = Position(70, 70)


def is_valid(position: Position) -> bool:
    return 0 <= position.x < WIDTH and 0 <= position.y < HEIGHT


def find_neighbors(position: Position) -> list[Position]:
    return [
        neighbor
        for neighbor in (position + direction for direction in DIRECTIONS)
        if is_valid(neighbor) and neighbor not in coordinates
    ]


def find_path(start: Position, end: Position) -> int | None:
    search_queue = PriorityQueue()
    search_queue.put(PrioritizedPosition(0, start))
    scores = {start: 0}

    while not search_queue.empty():
        current: Position = search_queue.get().position

        if current == end:
            return scores[current]

        for neighbor in find_neighbors(current):
            new_score = scores[current] + 1

            if neighbor not in scores or new_score < scores[neighbor]:
                scores[neighbor] = new_score
                search_queue.put(PrioritizedPosition(new_score, neighbor))

    return None


with open("input.txt", encoding="utf-8") as file:
    coordinate_input = [Position(*map(int, line.split(","))) for line in file.readlines()]

# Part 1.
coordinates = coordinate_input[:1024]
print(find_path(START, END))

# Part 2.
for position in coordinate_input[1024:]:
    coordinates.append(position)
    if find_path(START, END) is None:
        print(position)
        break
