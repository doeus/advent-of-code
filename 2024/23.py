from itertools import combinations


def find_triplet_cliques(computers: dict[str, set[str]]) -> set[frozenset[str]]:
    cliques = set()

    for a, connections in computers.items():
        for b, c in combinations(connections, 2):
            if {a, c} <= computers[b] and {a, b} <= computers[c]:
                cliques.add(frozenset({a, b, c}))

    return cliques


def find_maximum_clique(computers: dict[str, set[str]]) -> set[str]:
    maximum_clique = set()

    for a, connections in computers.items():
        clique = {a}

        for b in connections:
            if clique <= computers[b]:
                clique.add(b)

        maximum_clique = max(clique, maximum_clique, key=len)

    return maximum_clique


with open("input.txt", encoding="utf-8") as file:
    lines = list(map(str.strip, file.readlines()))

computers: dict[str, set[str]] = {}

for line in lines:
    a, b = line.split("-")
    computers.setdefault(a, set()).add(b)
    computers.setdefault(b, set()).add(a)

# Part 1.
print(sum(any(computer.startswith("t") for computer in clique) for clique in find_triplet_cliques(computers)))

# Part 2.
print(",".join(sorted(find_maximum_clique(computers))))
