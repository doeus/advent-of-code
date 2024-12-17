from collections import defaultdict, deque
from dataclasses import dataclass, field
from itertools import chain, pairwise
from queue import PriorityQueue


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def __add__(self, other: "Position") -> "Position":
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Position") -> "Position":
        return Position(self.x - other.x, self.y - other.y)


@dataclass(frozen=True)
class Node:
    position: Position
    direction: Position


@dataclass(order=True)
class PrioritizedNode:
    priority: int
    node: Node = field(compare=False)


DIRECTIONS = {"^": Position(0, -1), ">": Position(1, 0), "v": Position(0, 1), "<": Position(-1, 0)}


def calculate_node_score(source: Node, target: Position) -> int:
    return 1 if source.position + source.direction == target else 1001


def calculate_path_score(path: list[Node]) -> int:
    return sum(calculate_node_score(a, b.position) for a, b in pairwise(path))


def find_neighbors(position: Position) -> list[Position]:
    return [
        neighbor
        for neighbor in (position + direction for direction in DIRECTIONS.values())
        if maze[neighbor.y][neighbor.x] in {".", "E"}
    ]


def find_path(start: Position, end: Position) -> tuple[int, int]:
    search_queue = PriorityQueue()
    search_queue.put(PrioritizedNode(0, Node(start, DIRECTIONS[">"])))
    origins = defaultdict(dict)
    scores = {Node(start, DIRECTIONS[">"]): 0}
    min_score = 0

    while not search_queue.empty():
        current: Node = search_queue.get().node

        if current.position == end:
            min_score = scores[current]
            break

        for neighbor in find_neighbors(current.position):
            new_score = scores[current] + calculate_node_score(current, neighbor)
            node = Node(neighbor, neighbor - current.position)

            if node not in scores or new_score < scores[node]:
                scores[node] = new_score
                search_queue.put(PrioritizedNode(new_score, node))
                origins[node.position][current.position] = new_score

    paths = []

    def trace_path(path: deque[Position], current: Position, current_score: int) -> None:
        if current == start:
            directed_path = [Node(start, DIRECTIONS[">"])]
            directed_path.extend(Node(b, b - a) for a, b in pairwise(reversed(path)))
            paths.append(directed_path)
            return

        for previous, previous_score in origins[current].items():
            if previous_score <= current_score:
                path.append(previous)
                trace_path(path, previous, previous_score)
                path.pop()

    trace_path(deque([end]), end, min_score)

    min_paths = filter(lambda path: calculate_path_score(path) == min_score, paths)
    seats = set(chain.from_iterable({node.position for node in path} for path in min_paths))

    return (min_score, len(seats))


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

score, seat_count = find_path(start, end)

# Part 1.
print(score)

# Part 2.
print(seat_count)
