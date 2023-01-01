import operator
import cProfile

OPERATIONS = {"+": operator.add, "-": operator.sub, "*": operator.mul}
OLD_OPERAND = "old"
LEFT_OPERAND = "left"
RIGHT_OPERAND = "right"


FILENAME = "day11/input.txt"


def strip_punctuation(string):
    return int(string.translate(str.maketrans("", "", ", :")))


def map_operand(operand):
    return -1 if operand == OLD_OPERAND else int(operand)


class Monkey:
    def __init__(self, name, items, operation, test):
        self.name = name
        self.items = items
        self.test = test

        operation_components = operation.split(" ")
        self.operator = OPERATIONS[operation_components[1]]
        self.operands = {
            LEFT_OPERAND: map_operand(operation_components[0]),
            RIGHT_OPERAND: map_operand(operation_components[2]),
        }
        self.inspect_counter = 0
        self.least_common_multiple = None

    def __repr__(self):
        return f"Monkey({self.name}, {self.items}, {self.operands}, {self.test})"

    def __str__(self):
        return f"Monkey {self.name}: {[item for item in self.items]}"

    def receive_item(self, item):
        self.items.append(item)

    def perform_operation(self, item):
        return self.operator(
            item if self.operands[LEFT_OPERAND] == -1 else self.operands[LEFT_OPERAND],
            item
            if self.operands[RIGHT_OPERAND] == -1
            else self.operands[RIGHT_OPERAND],
        )

    def inspect_items(self):
        returned_items = []
        while self.items:
            item = self.items.pop(0)
            self.inspect_counter += 1
            inspected = self.perform_operation(item)
            inspected %= self.least_common_multiple

            # inspected = inspected // 3
            # print(f"Divided by 3: {inspected} (rounded down)")

            inspection_status = inspected % self.test["divisible"] == 0
            returned_items.append(
                {"item": inspected, "target": self.test[inspection_status]}
            )

        return returned_items


def show_gang(monkeys):
    for name in monkeys:
        print(monkeys[name])


def get_monkey_business(monkeys):
    top_two = sorted(
        monkeys, key=lambda monkey: monkeys[monkey].inspect_counter, reverse=True
    )[:2]
    return monkeys[top_two[0]].inspect_counter * monkeys[top_two[1]].inspect_counter


def load_input():
    monkeys = {}
    least_common_multiple = 1

    with open(FILENAME, "r") as f:
        all_input = [line.strip() for line in f.readlines()]

    monkey = {}
    for line in all_input:
        if line.startswith("Monkey "):
            monkey["name"] = strip_punctuation(line.split(" ")[1])
        elif line.startswith("Starting items: "):
            monkey["items"] = [strip_punctuation(item) for item in line.split(" ")[2:]]
        elif line.startswith("Operation: "):
            monkey["operation"] = line.split(" = ")[1]
        elif line.startswith("Test: "):
            monkey["test"] = {"divisible": int(line.split(" ")[-1])}
            least_common_multiple *= monkey["test"]["divisible"]
        elif line.startswith("If true: "):
            monkey["test"][True] = int(line.split(" ")[-1])
        elif line.startswith("If false: "):
            monkey["test"][False] = int(line.split(" ")[-1])

        if line == "":
            monkey = Monkey(**monkey)

            monkeys[monkey.name] = monkey
            monkey = {}
    else:
        monkey = Monkey(**monkey)
        monkeys[monkey.name] = monkey

    for monkey in monkeys:
        monkeys[monkey].least_common_multiple = least_common_multiple

    return monkeys


def run():
    monkeys = load_input()

    for _ in range(10000):
        for name in monkeys:
            items = monkeys[name].inspect_items()

            for item in items:
                monkeys[item["target"]].receive_item(item["item"])

        # show_gang(monkeys)

    for name in monkeys:
        print(f"Inspect counter: {monkeys[name].inspect_counter}")

    monkey_business = get_monkey_business(monkeys)
    print(f"Monkey business: {monkey_business}")


if __name__ == "__main__":
    cProfile.run("run()")
