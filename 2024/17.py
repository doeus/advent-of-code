import re


def execute(a: int, b: int, c: int, program: list[int]) -> list[int]:
    def get_combo_operand() -> int:
        match program[ip + 1]:
            case 4:
                return a
            case 5:
                return b
            case 6:
                return c
            case _:
                return program[ip + 1]

    ip = 0
    output: list[int] = []

    while ip < len(program):
        match program[ip]:
            case 0:
                a //= 2 ** get_combo_operand()
            case 1:
                b ^= program[ip + 1]
            case 2:
                b = get_combo_operand() % 8
            case 3:
                ip = program[ip + 1] - 2 if a != 0 else ip
            case 4:
                b ^= c
            case 5:
                output.append(get_combo_operand() % 8)
            case 6:
                b = a // 2 ** get_combo_operand()
            case 7:
                c = a // 2 ** get_combo_operand()

        ip += 2

    return output


def find_a(a: int, b: int, c: int, program: list[int]) -> int | None:
    a <<= 3

    for i in range(8):
        output = execute(a + i, b, c, program)

        if output == program or output == program[len(program) - len(output) :]:
            if output == program:
                return a + i

            result = find_a(a + i, b, c, program)

            if result is not None:
                return result

    return None


with open("input.txt", encoding="utf-8") as file:
    numbers = list(map(int, re.findall(r"\d+", file.read())))

# Part 1.
print(",".join(map(str, execute(numbers[0], numbers[1], numbers[2], numbers[3:]))))

# Part 2.
print(find_a(0, 0, 0, numbers[3:]))
