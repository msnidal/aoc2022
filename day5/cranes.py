FILENAME = "day5/input.txt"


class CrateStack:
    def __init__(self, crates: list = None) -> None:
        if crates is None:
            self.crates = []
        else:
            self.crates = crates

    def __str__(self) -> str:
        return str(self.crates)

    def print_top(self):
        if len(self.crates) > 0:
            return self.crates[-1]

    def stack(self, crate):
        self.crates.append(crate)

    def pop(self, count=1):
        if len(self.crates) > 0:
            return [self.crates.pop() for _ in range(min(len(self.crates), count))]

    def move(self, other, count=1):
        crates = self.pop(count)

        if crates is not None:
            for crate in reversed(crates):
                other.stack(crate)


def print_stacks(stacks):
    for index, stack in enumerate(stacks):
        print(f"Stack {index + 1}: {stack}")


def load_file():
    with open(FILENAME, "r") as f:
        input_lines = [line[:-1] for line in f.readlines()]

        boundary = input_lines.index("")
        length = len(input_lines[0])

        stacks = [CrateStack() for _ in range((length // 4) + 1)]

        for line in reversed(input_lines[: boundary - 1]):
            for index, column in enumerate(range(0, length, 4)):
                crate = line[column + 1]

                if crate != " ":
                    stacks[index].stack(crate)

        print_stacks(stacks)

        for move in input_lines[boundary + 1 :]:
            parts = move.split(" ")
            count = int(parts[1])
            source = int(parts[3])
            target = int(parts[5])

            print(f"Move {count} from {source} to {target}")

            stacks[source - 1].move(stacks[target - 1], count)
            # for _ in range(count):
            #  stacks[source - 1].move(stacks[target - 1])

            print_stacks(stacks)

        return stacks


if __name__ == "__main__":
    stacks = load_file()

    top_letters = f"{''.join([stack.print_top() for stack in stacks if stack.print_top() is not None])}"
    print(f"Top letters: {top_letters}")
    print_stacks(stacks)
