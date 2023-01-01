class Range:
    def __init__(self, lower_bound, upper_bound) -> None:
        self.range = {x for x in range(lower_bound, upper_bound + 1)}

    def __str__(self) -> str:
        return str(self.range)

    def contains(self, other):
        for value in other.range:
            if value not in self.range:
                return False

        return True

    def overlaps(self, other):
        for value in other.range:
            if value in self.range:
                return True

        return False


def load_data():
    with open("day4/input.txt", "r") as f:
        for line in f:
            left, right = line.strip().split(",")
            yield (
                Range(*map(int, left.split("-"))),
                Range(*map(int, right.split("-"))),
            )


if __name__ == "__main__":
    data = load_data()
    score = 0

    for left, right in data:
        # has_overlap = left.contains(right) or right.contains(left)
        has_overlap = left.overlaps(right) or right.overlaps(left)
        print(f"{left} contains {right}? {has_overlap}")
        if has_overlap:
            score += 1

    print(f"Score: {score}")
