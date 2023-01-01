import copy

FILENAME = "day9/input.txt"


def load_moves():
    moves = []
    with open(FILENAME, "r") as file:
        for line in file.readlines():
            (direction, length) = line.strip().split(" ")
            moves.append((direction, int(length)))

    return moves


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def follow(self, other):
        if self.is_adjacent(other):
            for axis in (0, 1):
                if other[axis] > self[axis] + 1:
                    self[axis] += 1
                    break
                elif other[axis] < self[axis] - 1:
                    self[axis] -= 1
                    break
        else:
            for axis in (0, 1):
                if self[axis] < other[axis]:
                    self[axis] += 1
                elif self[axis] > other[axis]:
                    self[axis] -= 1

    def is_adjacent(self, other):
        is_adjacent = abs(self.x - other.x) <= 1 and abs(self.y - other.y) <= 1
        return is_adjacent

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def __copy__(self):
        return self.__class__(self.x, self.y)

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError("Index must be 0 or 1")

    def __setitem__(self, index, value):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        else:
            raise IndexError("Index must be 0 or 1")


class Rope:
    def __init__(self, tails=1):
        self.head = Position(0, 0)
        self.tails = [Position(0, 0) for _ in range(tails)]

        self.tail_history = set()

    def move(self, direction, length):
        for _ in range(length):
            if direction == "R":
                self.head[0] += 1
            elif direction == "U":
                self.head[1] += 1
            elif direction == "L":
                self.head[0] -= 1
            elif direction == "D":
                self.head[1] -= 1

            next_segment = self.head
            for tail in self.tails:
                tail.follow(next_segment)
                next_segment = tail

            self.tail_history.add(copy.copy(tail))

    def get_position(self):
        return (self.x, self.y)

    def __str__(self) -> str:
        return f"(Head({self.head}), Tails({self.tails})"


if __name__ == "__main__":
    moves = load_moves()
    rope = Rope(9)

    for move in moves:
        rope.move(move[0], move[1])
        print(len(rope.tail_history))
