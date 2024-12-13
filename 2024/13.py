import re
from itertools import batched


def calculate_cost(a: tuple[int, int], b: tuple[int, int], t: tuple[int, int]) -> int:
    y = (t[1] * a[0] - t[0] * a[1]) / (b[1] * a[0] - b[0] * a[1])
    x = (t[0] - b[0] * y) / a[0]

    return int(x * 3 + y) if x.is_integer() else 0


with open("input.txt", encoding="utf-8") as file:
    machines = list(batched(batched(map(int, re.findall(r"\d+", file.read())), 2), 3))

# Part 1.
print(sum(calculate_cost(a, b, t) for a, b, t in machines))

# Part 2.
print(sum(calculate_cost(a, b, (t[0] + 10000000000000, t[1] + 10000000000000)) for a, b, t in machines))
