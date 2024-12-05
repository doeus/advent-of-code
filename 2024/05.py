from functools import cmp_to_key


def compare_pages(a: int, b: int) -> int:
    if [a, b] in rules:
        return -1
    if [b, a] in rules:
        return 1
    return 0


with open("input.txt", encoding="utf-8") as file:
    lines = file.readlines()

rules = [list(map(int, line.split("|"))) for line in lines if "|" in line]
updates = [list(map(int, line.split(","))) for line in lines if "," in line]

# Part 1.
print(sum(update[len(update) // 2] for update in updates if update == sorted(update, key=cmp_to_key(compare_pages))))

# Part 2.
print(
    sum(
        corrected_update[len(corrected_update) // 2]
        for update in updates
        if update != (corrected_update := sorted(update, key=cmp_to_key(compare_pages)))
    )
)
