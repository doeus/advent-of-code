with open("input.txt", encoding="utf-8") as file:
    matrix = [line.strip() for line in file.readlines()]

width = len(matrix[0])
height = len(matrix)

# Part 1.
p1 = 0

for y in range(height):
    for x in range(width):
        # Check horizontally.
        if x < width - 3:
            p1 += "".join(matrix[y][x + dx] for dx in range(4)) in ("XMAS", "SAMX")

        # Check vertically.
        if y < height - 3:
            p1 += "".join(matrix[y + dy][x] for dy in range(4)) in ("XMAS", "SAMX")

        # Check diagonally.
        if x < width - 3 and y < height - 3:
            p1 += "".join(matrix[y + dy][x + dx] for dx, dy in zip(range(4), range(4))) in ("XMAS", "SAMX")
            p1 += "".join(matrix[y + dy][x + dx] for dx, dy in zip(range(4), range(3, -1, -1))) in ("XMAS", "SAMX")

print(p1)

# Part 2.
p2 = 0

for y in range(height - 2):
    for x in range(width - 2):
        a = "".join(matrix[y + dy][x + dx] for dx, dy in zip(range(3), range(3)))
        b = "".join(matrix[y + dy][x + dx] for dx, dy in zip(range(3), range(2, -1, -1)))
        p2 += a in ("MAS", "SAM") and b in ("MAS", "SAM")

print(p2)
