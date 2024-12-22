from collections import defaultdict
from itertools import pairwise


def generate_secret_sequence(initial_secret: int, count: int) -> list[int]:
    secret_sequence = [initial_secret]

    for _ in range(count):
        initial_secret ^= initial_secret * 64
        initial_secret %= 16777216

        initial_secret ^= initial_secret // 32
        initial_secret %= 16777216

        initial_secret ^= initial_secret * 2048
        initial_secret %= 16777216

        secret_sequence.append(initial_secret)

    return secret_sequence


def generate_price_sequences(secret_sequence: list[int]) -> dict[tuple[int, int, int, int], int]:
    prices = [secret % 10 for secret in secret_sequence]
    price_changes = [b - a for a, b in pairwise(prices)]
    price_sequences = {}

    for i in range(len(price_changes) - 3):
        price_sequence = tuple(price_changes[i : i + 4])
        price = prices[i + 4]
        price_sequences.setdefault(price_sequence, price)

    return price_sequences


with open("input.txt", encoding="utf-8") as file:
    initial_secrets = list(map(int, file.readlines()))

# Part 1.
secret_sequences = [generate_secret_sequence(initial_secret, 2000) for initial_secret in initial_secrets]

print(sum(secret_sequence[-1] for secret_sequence in secret_sequences))

# Part 2.
combined_price_sequences = defaultdict(int)

for secret_sequence in secret_sequences:
    for price_sequence, price in generate_price_sequences(secret_sequence).items():
        combined_price_sequences[price_sequence] += price

print(max(combined_price_sequences.values()))
