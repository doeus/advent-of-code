from collections import Counter

with open("input.txt", encoding="utf-8") as file:
    lines = file.readlines()

left, right = zip(*(map(int, line.split()) for line in lines))

# Part 1.
print(sum(abs(x - y) for x, y in zip(sorted(left), sorted(right))))

# Part 2.
occurrences = Counter(right)
print(sum(x * occurrences[x] for x in left))
