from itertools import combinations

MIN_DIFFERENCE = 1
MAX_DIFFERENCE = 3


def is_increasing(levels: list[int]) -> bool:
    for i in range(len(levels) - 1):
        difference = levels[i + 1] - levels[i]
        if difference < MIN_DIFFERENCE or difference > MAX_DIFFERENCE:
            return False
    return True


with open("input.txt", encoding="utf-8") as file:
    lines = file.readlines()

reports = [list(map(int, line.split())) for line in lines]

# Part 1.
print(sum(is_increasing(report) or is_increasing(report[::-1]) for report in reports))

# Part 2.
print(
    sum(
        any(
            map(
                is_increasing,
                list(combinations(report, len(report) - 1)) + list(combinations(report[::-1], len(report) - 1)),
            )
        )
        for report in reports
    )
)
