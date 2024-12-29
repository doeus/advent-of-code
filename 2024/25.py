from itertools import product
from operator import add


def does_fit(lock: list[int], key: list[int]) -> bool:
    return all(height <= 5 for height in map(add, lock, key))


with open("input.txt", encoding="utf-8") as file:
    schematics = [schematic.splitlines() for schematic in file.read().split("\n\n")]

locks = []
keys = []

for schematic in schematics:
    heights = [column.count("#") - 1 for column in zip(*schematic)]

    if schematic[0] == "#####":
        locks.append(heights)
    else:
        keys.append(heights)

# Part 1.
print(sum(does_fit(lock, key) for lock, key in product(locks, keys)))
