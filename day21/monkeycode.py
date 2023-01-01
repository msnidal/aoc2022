import parse
import operator
import functools

TEMPLATES = ("{codename}: {operation}", "{left_operand} {operator} {right_operand}")
OPERATIONS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "=": operator.eq,
}


def load_monkeys(filename):
    monkeys = {}
    with open(filename) as file:
        chatter = [parse.parse(TEMPLATES[0], line.strip()) for line in file.readlines()]
        monkeys = {monkey["codename"]: monkey["operation"] for monkey in chatter}
        for monkey in monkeys:
            operation = parse.parse(TEMPLATES[1], monkeys[monkey])
            if operation:
                monkeys[monkey] = {
                    key: OPERATIONS[value] if key == "operator" else value
                    for key, value in operation.named.items()
                }
            else:
                monkeys[monkey] = {"axiom": int(monkeys[monkey])}

    return monkeys


def resolve_root(codename, monkeys):
    monkey = monkeys[codename]

    if "axiom" in monkey:
        return monkey["axiom"], codename == "humn"
    else:
        left_operand, left_chain = resolve_root(monkey["left_operand"], monkeys)
        right_operand, right_chain = resolve_root(monkey["right_operand"], monkeys)
        result = monkey["operator"](left_operand, right_operand)

        operator, chain = None, None
        if left_chain:
            chain = (
                left_chain if type(left_chain) == list else []
            )  # Start at level above human
            operator = lambda x: monkey["operator"](
                x, right_operand
            )  # Reverse the operator
            chain.append(operator)
        elif right_chain:
            chain = right_chain if type(right_chain) == list else []
            operator = functools.partial(monkey["operator"], left_operand)
            chain.append(operator)

        return result, chain


def apply_operation_chain(operator_chain, operand):
    for operation in operator_chain:
        print(f"Applying {operation} to {operand}")
        operand = operation(operand)

    return operand


if __name__ == "__main__":
    monkeys = load_monkeys("day21/input.txt")

    # Part 1:
    value, _ = resolve_root("root", monkeys)
    print(value)

    # Part 2:
    monkeys["root"]["operator"] = OPERATIONS["-"]  # Our solution is at zero
    _, operator_chain = resolve_root("root", monkeys)

    print(
        apply_operation_chain(operator_chain, 3587647562851)
    )  # Just iterated on operation chain until we got a result
