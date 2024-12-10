from collections import defaultdict
from dataclasses import dataclass


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def __add__(self, other: "Position") -> "Position":
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Position") -> "Position":
        return Position(self.x - other.x, self.y - other.y)


DIRECTIONS = (Position(0, -1), Position(1, 0), Position(0, 1), Position(-1, 0))


def is_valid(position: Position) -> bool:
    return 0 <= position.x < width and 0 <= position.y < height


def find_trails(trail: list[Position]) -> None:
    trailhead = trail[0]
    trailtail = trail[-1]

    for direction in DIRECTIONS:
        p = trailtail + direction

        if is_valid(p) and matrix[p.y][p.x] - matrix[trailtail.y][trailtail.x] == 1:
            if matrix[p.y][p.x] == 9:
                trails[(trailhead, p)] += 1
            else:
                find_trails(trail + [p])


with open("input.txt", encoding="utf-8") as file:
    matrix = [list(map(int, line.strip())) for line in file.readlines()]

width = len(matrix[0])
height = len(matrix)
trailheads = [Position(x, y) for y in range(height) for x in range(width) if matrix[y][x] == 0]
trails = defaultdict(int)

for trailhead in trailheads:
    find_trails([trailhead])

# Part 1.
print(len(trails))

# Part 2.
print(sum(trails.values()))
