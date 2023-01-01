import math

BEARINGS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
BEARING_LOOKUP = {
    "N": BEARINGS[0],
    "E": BEARINGS[1],
    "S": BEARINGS[2],
    "W": BEARINGS[3],
}

BEARING_SYMBOLS = {
    BEARINGS[0]: "^",
    BEARINGS[1]: ">",
    BEARINGS[2]: "v",
    BEARINGS[3]: "<",
}
BEARING_SCORES = {BEARINGS[0]: 3, BEARINGS[1]: 0, BEARINGS[2]: 1, BEARINGS[3]: 2}

ROTATION = {  # Maps relative bearing to relative rotation. Normally would do this with numpy matrix multiplication but sticking to corelib
    0: 0,
    90: 1,
    180: 2,
    270: 3,
}

CUBE_EDGES = {  # Maps current surface to relative bearing of next surface. Per above would be better solved with matrix math but hardcoding to go fast!! See test_walk to see how I came up with these
    0: {
        BEARINGS[0]: (5, 90),
        BEARINGS[3]: (3, 180),
    },
    1: {
        BEARINGS[0]: (5, 0),
        BEARINGS[1]: (4, 180),
        BEARINGS[2]: (2, 90),
    },
    2: {
        BEARINGS[1]: (1, 270),
        BEARINGS[3]: (3, 270),
    },
    3: {
        BEARINGS[0]: (2, 90),
        BEARINGS[3]: (0, 180),
    },
    4: {
        BEARINGS[1]: (1, 180),
        BEARINGS[2]: (5, 90),
    },
    5: {
        BEARINGS[1]: (4, 270),
        BEARINGS[2]: (1, 0),
        BEARINGS[3]: (0, 270),
    },
}

""" For the sample, lol. Also made with the test_walk function
CUBE_EDGES = {
    0: {
        BEARINGS[0]: (1, 180),
        BEARINGS[1]: (5, 180),
        BEARINGS[3]: (2, 270),
    },
    1: {
        BEARINGS[0]: (0, 180),
        BEARINGS[2]: (4, 180),
        BEARINGS[3]: (5, 90)
    },
    2: {
        BEARINGS[0]: (0, 90),
        BEARINGS[2]: (4, 270),
    },
    3: {
        BEARINGS[1]: (5, 90),
    },
    4: {
        BEARINGS[2]: (1, 180),
        BEARINGS[3]: (2, 90),
    },
    5: {
        BEARINGS[0]: (3, 270),
        BEARINGS[1]: (0, 180),
        BEARINGS[2]: (1, 270)
    }
}
"""


class MovementError(Exception):
    pass


def load_map(filename):
    with open(filename) as file:
        raw_map = [line[:-1] for line in file.readlines()]  # Don't include newline

    split_index = raw_map.index("")
    map_characters, sequence = raw_map[:split_index], raw_map[split_index + 1]

    prepared_map = Map(map_characters)

    # Break down sequence. Duck typing
    instructions = []
    buffer = [[], int]
    for character in sequence:
        if character.isdigit() != (buffer[1] == int):
            instructions.append(
                buffer[1]("".join(buffer[0]))
            )  # Apply the type to the buffer!
            buffer[0].clear()
            buffer[1] = int if character.isdigit() else str

        buffer[0].append(character)

    instructions.append(buffer[1]("".join(buffer[0])))

    return prepared_map, instructions


class Map:
    def __init__(self, map_characters):
        self.prepared_map = map_characters

        self.set_starting_position()
        self.partition_map()
        self.show_partitions()

    def partition_map(self):
        """Partition the flat map into a cube"""
        widest_length = max([len(line) for line in self.prepared_map])
        height = len(self.prepared_map)
        partitions = []
        self.partition_lookup = dict()  # Map flat coordinate to partition number
        self.partitions = (
            dict()
        )  # Map partition number to local surface coordinate grid

        # Find the surface dimension dynamically to handle sample and input
        self.surface_dimension = math.gcd(widest_length, height)

        for y in range(height):
            row_length = len(self.prepared_map[y])
            for x in range(row_length):
                partition_coordinate = (y // self.surface_dimension) * (
                    widest_length // self.surface_dimension
                ) + (
                    x // self.surface_dimension
                )  # Partition coordinate includes blank areas - maps to partition index below
                if self.prepared_map[y][x] != " ":
                    if partition_coordinate not in partitions:
                        partitions.append(partition_coordinate)

                    partition_index = partitions.index(partition_coordinate)
                    self.partition_lookup[(y, x)] = partition_index

                    if partition_index not in self.partitions:
                        self.partitions[partition_index] = dict()
                    self.partitions[partition_index][
                        (y % self.surface_dimension, x % self.surface_dimension)
                    ] = (y, x)

        # We're using plenty of memory here but to make our lives easier we also generate an inverse partition map
        self.partition_inverse = {
            index: {v: k for k, v in partition.items()}
            for index, partition in self.partitions.items()
        }

    def set_starting_position(self):
        """Set inplace y, x coordinate of topmost, leftmost open space"""
        position = (0, self.prepared_map[0].index("."))
        bearing = BEARING_LOOKUP["E"]

        self.path = [[position, bearing]]

    def get_wrapped_position(self, position, bearing):
        """Return the position wrapped around the map, in the opposite direction of the bearing
        Overshoot by one to make the navigate loop easier
        """

        # Part 1 logic:
        """
        while True:
            try:
                position = self.increment_position(position, bearing, reverse=True)
                tile = self.prepared_map[position[0]][
                    position[1]
                ]  # Will raise indexerror if outside bounds
                if tile == " ":
                    raise IndexError("Out of map. Loop")
            except IndexError:
                return position
        """

        # Part 2 logic:
        current_face = self.partition_lookup[position]
        local_coordinate = self.partition_inverse[current_face][position]
        destination_face, angle = CUBE_EDGES[current_face][bearing]
        projection = BEARINGS[ROTATION[angle]]

        other_surface = self.partitions[destination_face]
        projected_coordinate = self.project_coordinates(
            local_coordinate, bearing, projection
        )

        new_bearing = BEARINGS[(BEARINGS.index(bearing) + ROTATION[angle]) % 4]

        return other_surface[projected_coordinate], new_bearing

    def project_coordinates(self, coordinates, bearing, projection):
        """Rotate and return a coordinate grid 90 degrees clockwise by the given number of rotations"""

        naive_coordinate = tuple(
            dimension % self.surface_dimension
            for dimension in self.increment_position(coordinates, bearing, wrap=True)
        )

        if projection == BEARING_LOOKUP["N"]:
            projected_coordinates = naive_coordinate
        elif projection == BEARING_LOOKUP["E"]:
            projected_coordinates = (
                naive_coordinate[1],
                self.surface_dimension - naive_coordinate[0] - 1,
            )
        elif projection == BEARING_LOOKUP["S"]:
            projected_coordinates = (
                self.surface_dimension - naive_coordinate[0] - 1,
                self.surface_dimension - naive_coordinate[1] - 1,
            )
        elif projection == BEARING_LOOKUP["W"]:
            projected_coordinates = (
                self.surface_dimension - naive_coordinate[1] - 1,
                naive_coordinate[0],
            )

        return projected_coordinates

    def increment_position(self, position, bearing, wrap=False, reverse=False):
        """Return the position incremented by one in the bearing direction"""
        next_position = (
            (position[0] + bearing[0], position[1] + bearing[1])
            if not reverse
            else (position[0] - bearing[0], position[1] - bearing[1])
        )
        # Normalize negative indices
        if not wrap:
            if next_position[0] < 0 or next_position[1] < 0:
                raise IndexError("Out of map. Loop")
        else:
            next_position = (
                next_position[0] % len(self.prepared_map),
                next_position[1] % len(self.prepared_map[0]),
            )

        return next_position

    def navigate(self, instruction, ignore_walls=False):
        # Turn around
        position, bearing = self.path[-1]

        if instruction == "L":
            self.path[-1][1] = BEARINGS[(BEARINGS.index(bearing) - 1) % len(BEARINGS)]
        elif instruction == "R":
            self.path[-1][1] = BEARINGS[(BEARINGS.index(bearing) + 1) % len(BEARINGS)]

        # Move
        elif type(instruction) == int:
            remaining = instruction
            while remaining > 0:
                try:
                    next_position = self.increment_position(position, bearing)
                    tile = self.prepared_map[next_position[0]][
                        next_position[1]
                    ]  # Will raise indexerror if outside bounds
                    if tile == " ":
                        raise IndexError("Out of map. Loop")
                    else:
                        next_bearing = bearing
                except IndexError:
                    next_position, next_bearing = self.get_wrapped_position(
                        position, bearing
                    )
                    tile = self.prepared_map[next_position[0]][next_position[1]]
                finally:
                    if tile == "#" and not ignore_walls:  # Hit wall. Stay put
                        remaining = 0
                    else:
                        self.path.append([next_position, next_bearing])
                        position, bearing = next_position, next_bearing
                        remaining -= 1

    def get_score(self):
        position, bearing = self.path[-1]
        return (
            1000 * (position[0] + 1) + 4 * (position[1] + 1) + BEARING_SCORES[bearing]
        )

    def show_partitions(self):
        for y in range(len(self.prepared_map)):
            for x in range(len(self.prepared_map[y])):
                if (y, x) in self.partition_lookup:
                    print(self.partition_lookup[(y, x)], end="")
                else:
                    print(" ", end="")
            print()

    def test_walk(self):
        """Because the cube edge logic is messy we want to validate that from any point we can walk in a straight line and return to where we started
        Heavy but useful for debugging!
        """

        for (y, x) in self.partition_lookup:
            for bearing in BEARINGS:
                self.path = [[(y, x), bearing]]
                self.navigate(self.surface_dimension * 4, ignore_walls=True)
                assert self.path[-1] == self.path[0], f"Failed at {y}, {x}, {bearing}"

        self.set_starting_position()

    def __str__(self):
        rendered_map = self.prepared_map.copy()
        for ((y, x), bearing) in self.path:
            symbol = BEARING_SYMBOLS[bearing]
            rendered_map[y] = rendered_map[y][:x] + symbol + rendered_map[y][x + 1 :]

        return "Map:\n" + "\n".join(rendered_map)


if __name__ == "__main__":
    prepared_map, sequence = load_map("day22/input.txt")
    print(prepared_map)

    # Assert that the map is valid
    prepared_map.test_walk()

    for command in sequence:
        # print(command)
        prepared_map.navigate(command)
        # print(prepared_map)

    print(prepared_map)
    print(prepared_map.get_score())
