from collections import defaultdict
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


@dataclass(order=True)
class PrioritizedPosition:
    priority: int
    position: Position = field(compare=False)


DIRECTIONS = (Position(0, -1), Position(1, 0), Position(0, 1), Position(-1, 0))


def calculate_distance(a: Position, b: Position) -> int:
    return abs(b.x - a.x) + abs(b.y - a.y)


def is_valid(position: Position) -> bool:
    return 0 <= position.x < width and 0 <= position.y < height


def find_neighbors(position: Position) -> list[Position]:
    return [
        neighbor
        for neighbor in (position + direction for direction in DIRECTIONS)
        if is_valid(neighbor) and maze[neighbor.y][neighbor.x] != "#"
    ]


def find_path(start: Position, end: Position) -> list[Position]:
    search_queue = PriorityQueue()
    search_queue.put(PrioritizedPosition(0, start))
    scores = {start: 0}
    origins = {start: None}

    while not search_queue.empty():
        current: Position = search_queue.get().position

        if current == end:
            break

        for neighbor in find_neighbors(current):
            new_score = scores[current] + 1

            if neighbor not in scores or new_score < scores[neighbor]:
                scores[neighbor] = new_score
                search_queue.put(PrioritizedPosition(new_score, neighbor))
                origins[neighbor] = current

    if end not in origins:
        return []

    path = []
    current = end

    while current is not None:
        path.append(current)
        current = origins[current]

    return list(reversed(path))


def calculate_cheat_gains(path: list[Position], cheat_distance: int) -> dict[int, int]:
    original_distance = len(path) - 1
    distance_from_start = {position: distance for distance, position in enumerate(path)}
    distance_to_end = {position: distance for distance, position in enumerate(reversed(path))}
    cheat_gains = defaultdict(int)

    for i, current_position in enumerate(path[:-1]):
        for next_position in reversed(path[i + 1 :]):
            if (distance := calculate_distance(current_position, next_position)) <= cheat_distance:
                new_distance = distance_from_start[current_position] + distance_to_end[next_position] + distance
                cheat_gains[original_distance - new_distance] += 1

    return cheat_gains


with open("input.txt", encoding="utf-8") as file:
    maze = [list(line.strip()) for line in file.readlines()]

width = len(maze[0])
height = len(maze)
start = None
end = None

for y in range(height):
    for x in range(width):
        if maze[y][x] == "S":
            start = Position(x, y)

        if maze[y][x] == "E":
            end = Position(x, y)

        if start and end:
            break

path = find_path(start, end)

# Part 1.
print(sum(count for cheat_gain, count in calculate_cheat_gains(path, 2).items() if cheat_gain >= 100))

# Part 2.
print(sum(count for cheat_gain, count in calculate_cheat_gains(path, 20).items() if cheat_gain >= 100))
