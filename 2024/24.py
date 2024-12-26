from dataclasses import dataclass


@dataclass(frozen=True)
class Gate:
    left_wire_name: str
    right_wire_name: str
    output_wire_name: str
    operator: str

    @property
    def is_input(self) -> bool:
        return self.left_wire_name[0] in {"x", "y"} and self.right_wire_name[0] in {"x", "y"}

    @property
    def is_output(self) -> bool:
        return self.output_wire_name[0] == "z"


def simulate(gate: Gate) -> bool:
    if gate.left_wire_name not in wires:
        simulate(gates[gate.left_wire_name])

    if gate.right_wire_name not in wires:
        simulate(gates[gate.right_wire_name])

    match gate.operator:
        case "AND":
            wires[gate.output_wire_name] = wires[gate.left_wire_name] & wires[gate.right_wire_name]
        case "OR":
            wires[gate.output_wire_name] = wires[gate.left_wire_name] | wires[gate.right_wire_name]
        case "XOR":
            wires[gate.output_wire_name] = wires[gate.left_wire_name] ^ wires[gate.right_wire_name]

    return wires[gate.output_wire_name]


with open("input.txt", encoding="utf-8") as file:
    wire_data, gate_data = file.read().split("\n\n")

wires: dict[str, bool] = {}

for wire in wire_data.splitlines():
    name, value = wire.split(": ")
    wires[name] = bool(int(value))

gates: dict[str, Gate] = {}

for gate in gate_data.splitlines():
    left_wire_name, operator, right_wire_name, _, output_wire_name = gate.split(" ")
    gates[output_wire_name] = Gate(left_wire_name, right_wire_name, output_wire_name, operator)

# Part 1.
output = 0

for gate in (gate for name, gate in sorted(gates.items(), reverse=True) if name[0] == "z"):
    output <<= 1
    output += simulate(gate)

print(output)

# Part 2.
invalid_gates: set[Gate] = set()

for name, gate in gates.items():
    if gate.is_output and name != "z45" and gate.operator != "XOR":
        invalid_gates.add(gate)
        continue

    if name == "z45" and gate.operator != "OR":
        invalid_gates.add(gate)
        continue

    if not gate.is_input and not gate.is_output and gate.operator == "XOR":
        invalid_gates.add(gate)
        continue

    if gate.is_input and gate.operator == "AND" and "x00" not in {gate.left_wire_name, gate.right_wire_name}:
        if not any(
            name in {next_gate.left_wire_name, next_gate.right_wire_name}
            for next_gate in gates.values()
            if next_gate.operator == "OR"
        ):
            invalid_gates.add(gate)
            continue

    if gate.is_input and gate.operator == "XOR" and gate.output_wire_name != "z00":
        if not any(
            name in {next_gate.left_wire_name, next_gate.right_wire_name}
            for next_gate in gates.values()
            if next_gate.operator == "XOR"
        ):
            invalid_gates.add(gate)

print(",".join(sorted(invalid_gate.output_wire_name for invalid_gate in invalid_gates)))
