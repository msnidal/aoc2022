import copy


def load_numbers(filename, apply_key=False):
    with open(filename) as file:
        numbers = [
            int(line.strip()) * (811589153 if apply_key else 1)
            for line in file.readlines()
        ]

    return Mixer(numbers)


class Mixer:
    def __init__(self, numbers):
        self.sequence = numbers
        self.indices = [index for index in range(len(numbers))]

    def shift(self, index, debug=False):
        projected_index = self.indices.index(index)
        value = self.sequence[projected_index]

        destination = (projected_index + value) % (
            len(self) - 1
        )  # Wrap around one step before each edge!

        self.sequence.pop(projected_index)
        self.sequence.insert(destination, value)
        self.indices.pop(projected_index)
        self.indices.insert(destination, index)

        if debug:
            print(
                f"{value} moves between {self.sequence[(destination - 1) % len(self)]} and {self.sequence[(destination + 1) % len(self)]}"
            )
            print(self.sequence, "\n")

    def locate_grove(self, debug=False):
        zero_index = self.sequence.index(0)
        coordinates = [
            self.sequence[(coordinate + zero_index) % len(self)]
            for coordinate in (1000, 2000, 3000)
        ]

        if debug:
            print(f"Grove coordinates are {coordinates}")

        return sum(coordinates)

    def __repr__(self) -> str:
        return str(self.sequence)

    def __len__(self) -> int:
        return len(self.sequence)


if __name__ == "__main__":
    mixer = load_numbers("day20/input.txt", apply_key=True)

    for index in mixer.indices.copy() * 10:
        mixer.shift(index, debug=False)

    print(mixer.locate_grove(True))
