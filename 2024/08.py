from dataclasses import dataclass
from itertools import combinations


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def __add__(self, other: "Position") -> "Position":
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Position") -> "Position":
        return Position(self.x - other.x, self.y - other.y)


def is_valid(position: Position) -> bool:
    return 0 <= position.x < width and 0 <= position.y < height


with open("input.txt", encoding="utf-8") as file:
    matrix = [line.strip() for line in file.readlines()]

width = len(matrix[0])
height = len(matrix)
antennas = (Position(x, y) for y in range(height) for x in range(width) if matrix[y][x] != ".")
antenna_pairs = [(a, b) for a, b in combinations(antennas, 2) if matrix[a.y][a.x] == matrix[b.y][b.x]]

# Part 1.
antinodes = set()

for a, b in antenna_pairs:
    difference = b - a

    antinode = a - difference
    if is_valid(antinode):
        antinodes.add(antinode)

    antinode = b + difference
    if is_valid(antinode):
        antinodes.add(antinode)

print(len(antinodes))

# Part 2.
antinodes = set()

for a, b in antenna_pairs:
    difference = b - a

    antinode = a
    while is_valid(antinode):
        antinodes.add(antinode)
        antinode -= difference

    antinode = a + difference
    while is_valid(antinode):
        antinodes.add(antinode)
        antinode += difference

print(len(antinodes))
