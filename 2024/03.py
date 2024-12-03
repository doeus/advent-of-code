import re

with open("input.txt", encoding="utf-8") as file:
    data = file.read()

# Part 1.
instructions = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", data)

print(sum(int(x) * int(y) for x, y in instructions))

# Part 2.
instructions = re.findall(r"(mul)\((\d{1,3}),(\d{1,3})\)|(do)\(|(don't)\(", data)

do = True
result = 0
for instruction in instructions:
    if instruction[3]:
        do = True
    elif instruction[4]:
        do = False
    else:
        if do:
            result += int(instruction[1]) * int(instruction[2])

print(result)
