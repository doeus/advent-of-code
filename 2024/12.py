from collections import deque
from dataclasses import dataclass
from itertools import pairwise


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def __add__(self, other: "Position") -> "Position":
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Position") -> "Position":
        return Position(self.x - other.x, self.y - other.y)


DIRECTIONS = [Position(0, -1), Position(1, 0), Position(0, 1), Position(-1, 0)]


def is_valid(position: Position) -> bool:
    return 0 <= position.x < width and 0 <= position.y < height


def is_same_region(left: Position, right: Position) -> bool:
    return is_valid(left) and is_valid(right) and garden[left.y][left.x] == garden[right.y][right.x]


def is_different_region(left: Position, right: Position) -> bool:
    return not is_same_region(left, right)


def find_regions() -> list[set[Position]]:
    plots = {Position(x, y) for y in range(height) for x in range(width)}
    regions = []

    while len(plots):
        queue = deque([plots.pop()])
        region = set()

        while len(queue):
            plot = queue.popleft()
            region.add(plot)

            for direction in DIRECTIONS:
                other = plot + direction

                if is_same_region(plot, other) and other not in region and other not in queue:
                    queue.append(other)

        plots -= region
        regions.append(region)

    return regions


def calculate_perimeter(region: set[Position]) -> int:
    perimeter = 0

    for plot in region:
        for direction in DIRECTIONS:
            perimeter += is_different_region(plot, plot + direction)

    return perimeter


def calculate_sides(region: set[Position]) -> int:
    sides = 0

    for plot in region:
        for direction_a, direction_b in pairwise(DIRECTIONS + [DIRECTIONS[0]]):
            sides += is_different_region(plot, plot + direction_a) and is_different_region(plot, plot + direction_b)
            sides += (
                is_same_region(plot, plot + direction_a)
                and is_same_region(plot, plot + direction_b)
                and is_different_region(plot, plot + direction_a + direction_b)
            )

    return sides


with open("input.txt", encoding="utf-8") as file:
    garden = [list(line.strip()) for line in file.readlines()]

width = len(garden[0])
height = len(garden)
regions = find_regions()

# Part 1.
print(sum(calculate_perimeter(region) * len(region) for region in regions))

# Part 2.
print(sum(calculate_sides(region) * len(region) for region in regions))
