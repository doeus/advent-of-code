from collections import Counter, defaultdict


def simulate(stones: dict[int, int], depth: int) -> dict[int, int]:
    for _ in range(depth):
        result = defaultdict(int)

        for stone, count in stones.items():
            if stone == 0:
                result[1] += count
            elif len(stone_str := str(stone)) % 2 == 0:
                result[int(stone_str[: len(stone_str) // 2])] += count
                result[int(stone_str[len(stone_str) // 2 :])] += count
            else:
                result[stone * 2024] += count

        stones = result

    return stones


with open("input.txt", encoding="utf-8") as file:
    stones = Counter(map(int, file.readline().split()))

# Part 1.
print(sum(simulate(stones, 25).values()))

# Part 2.
print(sum(simulate(stones, 75).values()))
