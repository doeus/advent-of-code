DIRECTIONS = {"^": (0, -1), ">": (1, 0), "v": (0, 1), "<": (-1, 0)}


def simulate(matrix: list[list[str]]) -> set[tuple[int, int]] | None:
    route = set()
    position = initial_position
    direction = initial_direction

    while 0 <= position[0] < width and 0 <= position[1] < height:
        if (position, direction) in route:
            return None

        route.add((position, direction))

        new_position = (position[0] + direction[0], position[1] + direction[1])
        if not (0 <= new_position[0] < width and 0 <= new_position[1] < height):
            break

        while matrix[new_position[1]][new_position[0]] == "#":
            if direction == DIRECTIONS["^"]:
                direction = DIRECTIONS[">"]
            elif direction == DIRECTIONS[">"]:
                direction = DIRECTIONS["v"]
            elif direction == DIRECTIONS["v"]:
                direction = DIRECTIONS["<"]
            else:
                direction = DIRECTIONS["^"]

            new_position = (position[0] + direction[0], position[1] + direction[1])
            if not (0 <= new_position[0] < width and 0 <= new_position[1] < height):
                break

        position = new_position

    return set(position for position, _ in route)


with open("input.txt", encoding="utf-8") as file:
    matrix = [list(line.strip()) for line in file.readlines()]

width = len(matrix[0])
height = len(matrix)

for x, y in ((x, y) for y in range(height) for x in range(width)):
    if matrix[y][x] in DIRECTIONS:
        initial_position = (x, y)
        initial_direction = DIRECTIONS[matrix[y][x]]
        break

positions = simulate(matrix)

# Part 1.
print(len(positions))

# Part 2.
loops = 0

for x, y in positions:
    if matrix[y][x] == ".":
        matrix[y][x] = "#"
        loops += simulate(matrix) is None
        matrix[y][x] = "."

print(loops)
