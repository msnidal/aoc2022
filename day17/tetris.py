X_BOUNDS = (0, 7)


class Piece:
    def __init__(self, shape, coordinates):
        self.shape = shape
        self.y, self.x = coordinates

    def __str__(self):
        return f"Piece({self.shape}, {self.x}, {self.y})"

    def shift(self, dx, dy):
        x = max(X_BOUNDS[0], min(self.x + dx, X_BOUNDS[1] - len(self.shape[0])))
        y = self.y + dy

        return Piece(self.shape, (y, x))

    def coordinates(self):
        for y, row in enumerate(reversed(self.shape)):
            for x, character in enumerate(row):
                if character:
                    yield (y + self.y, x + self.x)


class Board:
    def __init__(self, grid=None):
        if not grid:
            grid = set()

        self.grid = grid
        self.height = self.get_height()
        self.width = X_BOUNDS[1]

    def __contains__(self, piece: Piece):
        for coordinate in piece.coordinates():
            if coordinate[0] < 0 or coordinate[1] < 0 or coordinate[1] >= self.width:
                return True  # Out of bounds
            elif coordinate in self.grid:
                return True

        return False

    def get_height(self):
        return max(coordinate[0] for coordinate in self.grid | set([(-1, 0)])) + 1

    def insert(self, piece: Piece):
        self.grid |= set(piece.coordinates())
        self.height = self.get_height()

    def including_piece(self, piece: Piece):
        return Board(self.grid | set(piece.coordinates()))

    def __str__(self):
        rows = []
        for y in range(self.height + 3):
            row = []
            for x in range(self.width):
                if (y, x) in self.grid:
                    row.append("#")
                else:
                    row.append(".")
            rows.insert(0, "".join(row))

        board = "\n".join(rows)
        return f"Board\n{board}\n{'=' * self.width}"

    def get_spawn_coordinate(self, shape):
        # shape_height_offset = len(shape) - 1
        return (self.height + 3, 2)


def load_shapes(filename):
    shapes = []
    with open(filename) as file:
        shape = []
        for line in file:
            stripped = line.strip()
            if stripped == "":
                shapes.append(shape)
                shape = []
            else:
                shape.append(
                    [True if character == "#" else False for character in stripped]
                )

        shapes.append(shape)

    return shapes


def load_stream(filename):
    with open(filename) as file:
        stream = [-1 if character == "<" else 1 for character in file.read().strip()]

    return stream


def drop_pieces(board, shapes, stream):
    stream_index = 0

    for piece_index in range(10000):
        shape = shapes[piece_index % len(shapes)]
        coordinates = board.get_spawn_coordinate(shape)

        piece = Piece(shape, coordinates)
        target = piece
        while target not in board:
            # Apply air current
            stream_shift = stream[stream_index]
            stream_index = (stream_index + 1) % len(stream)

            target = piece.shift(stream_shift, 0)
            if target not in board:
                piece = target

            # Apply gravity
            target = piece.shift(0, -1)
            if target not in board:
                piece = target
            else:
                board.insert(piece)

            # print(board.including_piece(piece))


if __name__ == "__main__":
    shapes = load_shapes("day17/shapes.txt")
    stream = load_stream("day17/sample.txt")

    board = Board()

    drop_pieces(board, shapes, stream)
    print(board.get_height())
