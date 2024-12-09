from itertools import chain


def calculate_checksum(disk: list[int | None]) -> int:
    return sum(index * file_id for index, file_id in enumerate(disk) if file_id is not None)


with open("input.txt", encoding="utf-8") as file:
    disk = [(None if index % 2 else index // 2, int(length)) for index, length in enumerate(file.readline())]

# Part 1.
compacted_disk = list(chain.from_iterable([file_id] * length for file_id, length in disk))

i = 0
j = len(compacted_disk) - 1

while i < j:
    while i < j and compacted_disk[i] is not None:
        i += 1

    while i < j and compacted_disk[j] is None:
        j -= 1

    compacted_disk[i], compacted_disk[j] = compacted_disk[j], compacted_disk[i]
    i += 1
    j -= 1

print(calculate_checksum(compacted_disk))

# Part 2.
compacted_disk = disk

for j in range(len(compacted_disk) - 1, -1, -1):
    source = compacted_disk[j]

    if source[0] is None:
        continue

    for i in range(j):
        target = compacted_disk[i]

        if target[0] is None and target[1] >= source[1]:
            compacted_disk[i] = (None, target[1] - source[1])
            compacted_disk[j] = (None, source[1])
            compacted_disk.insert(i, source)
            break

compacted_disk = list(chain.from_iterable([file_id] * length for file_id, length in compacted_disk))
print(calculate_checksum(compacted_disk))
