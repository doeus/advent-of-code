import re
from collections import Counter, deque
from dataclasses import dataclass
from itertools import batched


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def __add__(self, other: "Position") -> "Position":
        return Position((self.x + other.x) % WIDTH, (self.y + other.y) % HEIGHT)

    def __mul__(self, factor: int) -> "Position":
        return Position(self.x * factor, self.y * factor)


@dataclass
class Robot:
    position: Position
    velocity: Position


DIRECTIONS = [Position(0, -1), Position(1, 0), Position(0, 1), Position(-1, 0)]
WIDTH = 101
HEIGHT = 103
EASTER_EGG_THRESHOLD = 20


def simulate(room: list[Robot], depth: int) -> list[Robot]:
    return [Robot(robot.position + robot.velocity * depth, robot.velocity) for robot in room]


def calculate_safety_factor(room: list[Robot]) -> int:
    positions = Counter(robot.position for robot in room)

    q1 = 0
    q2 = 0
    q3 = 0
    q4 = 0

    for position, count in positions.items():
        q1 += (position.x < WIDTH // 2 and position.y < HEIGHT // 2) * count
        q2 += (position.x > WIDTH // 2 and position.y < HEIGHT // 2) * count
        q3 += (position.x > WIDTH // 2 and position.y > HEIGHT // 2) * count
        q4 += (position.x < WIDTH // 2 and position.y > HEIGHT // 2) * count

    return q1 * q2 * q3 * q4


def is_easter_egg(positions: set[Position]) -> bool:
    while len(positions):
        queue = deque([positions.pop()])
        visited = set()

        while len(queue):
            p = queue.popleft()
            visited.add(p)

            if len(visited) > EASTER_EGG_THRESHOLD:
                return True

            for direction in DIRECTIONS:
                q = p + direction

                if q not in visited and q in positions:
                    positions.remove(q)
                    queue.append(q)

    return False


def find_easter_egg(room: list[Robot]) -> int | None:
    for i in range(WIDTH * HEIGHT):
        room = simulate(room, 1)
        if is_easter_egg({robot.position for robot in room}):
            return i + 1

    return None


with open("input.txt", encoding="utf-8") as file:
    room = [
        Robot(Position(*position), Position(*velocity))
        for position, velocity in batched(batched(map(int, re.findall(r"-?\d+", file.read())), 2), 2)
    ]

# Part 1.
print(calculate_safety_factor(simulate(room, 100)))

# Part 2.
print(find_easter_egg(room))
