import parse

NOTHINGNESS = "."
LIGHT = "#"
SENSOR = "S"
BEACON = "B"

FILENAME = "day15/input.txt"


def load_instructions():
    """ie.
    Sensor at x=20, y=1: closest beacon is at x=15, y=3
    """
    instructions = []

    with open(FILENAME, "r") as file:
        for instruction in file.read().splitlines():
            sensor_x, sensor_y, beacon_x, beacon_y = parse.parse(
                "Sensor at x={}, y={}: closest beacon is at x={}, y={}", instruction
            )

            instructions.append(
                {
                    "sensor": (int(sensor_x), int(sensor_y)),
                    "beacon": (int(beacon_x), int(beacon_y)),
                }
            )

    return instructions


def get_manhattan_distance(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


class Grid:
    def __init__(self, instructions, row_index):
        self.instructions = (
            instructions  # Useful to keep for iteration instead of checking every tile
        )
        self.boundaries = {}
        self.row_index = row_index

        for instruction in self.instructions:
            for component in instruction.values():  # Both beacons and sensors
                if (
                    "min_y" not in self.boundaries
                    or component[1] < self.boundaries["min_y"]
                ):
                    self.boundaries["min_y"] = component[1]
                if (
                    "max_y" not in self.boundaries
                    or component[1] > self.boundaries["max_y"]
                ):
                    self.boundaries["max_y"] = component[1]
                if (
                    "min_x" not in self.boundaries
                    or component[0] < self.boundaries["min_x"]
                ):
                    self.boundaries["min_x"] = component[0]
                if (
                    "max_x" not in self.boundaries
                    or component[0] > self.boundaries["max_x"]
                ):
                    self.boundaries["max_x"] = component[0]

        for instruction in self.instructions:
            instruction["range"] = get_manhattan_distance(
                instruction["sensor"], instruction["beacon"]
            )
            print(instruction)

    def check_row(self):
        # row = self.grid[row_index - self.boundaries["min_y"]]

        count_known = 0
        for x in range(
            self.boundaries["min_x"] - 1000000, self.boundaries["max_x"] + 1000000
        ):
            for instruction in self.instructions:
                if (
                    abs(instruction["sensor"][1] - self.row_index)
                    <= instruction["range"]
                ):
                    if (
                        get_manhattan_distance(
                            instruction["sensor"], (x, self.row_index)
                        )
                        <= instruction["range"]
                    ):
                        # print(f"Sensor {instruction['sensor']} is in range of tile {x}")
                        count_known += 1
                        break
            else:
                pass
                # print(f"No sensor is in range of tile {x}")

        # V. hacky but im tired lol
        beacons = {instruction["beacon"] for instruction in self.instructions}
        for beacon in beacons:
            if self.row_index == beacon[1]:
                # print(f"Beacon {instruction['beacon']} is within the row {x}")
                count_known -= 1

        return count_known


def get_adjacent_tiles(sensor, sensor_range, lower_bound, upper_bound):
    adjacency = set()

    extremities = {
        "top": sensor[1] + sensor_range,
        "bottom": sensor[1] - sensor_range,
        "left": sensor[0] - sensor_range,
        "right": sensor[0] + sensor_range,
    }

    # Get all of the tiles outside the diamond shape to find the intersection, lol
    for index, y in enumerate(range(extremities["bottom"] - 1, sensor[1])):
        if y < lower_bound or y > upper_bound:
            continue

        width = index

        if sensor[0] - width >= lower_bound and sensor[0] - width <= upper_bound:
            adjacency.add((sensor[0] - width, y))
        if sensor[0] + width >= lower_bound and sensor[0] + width <= upper_bound:
            adjacency.add((sensor[0] + width, y))

    for index, y in enumerate(range(sensor[1], extremities["top"] + 2)):
        if y < lower_bound or y > upper_bound:
            continue

        width = sensor_range - index

        if sensor[0] - width >= lower_bound and sensor[0] - width <= upper_bound:
            adjacency.add((sensor[0] - width, y))
        if sensor[0] + width >= lower_bound and sensor[0] + width <= upper_bound:
            adjacency.add((sensor[0] + width, y))

    return adjacency


def find_unknown_beacon(lower_bound, upper_bound, instructions):
    all_sets = []
    for instruction in instructions:
        all_sets.append(
            get_adjacent_tiles(
                instruction["sensor"], instruction["range"], lower_bound, upper_bound
            )
        )

    candidates = {}
    for border_set in all_sets:
        for comparable in all_sets:
            if border_set != comparable:
                for boundary_tile in border_set.intersection(comparable):
                    if boundary_tile not in candidates:
                        candidates[boundary_tile] = 1
                    else:
                        candidates[boundary_tile] += 1

    for candidate in sorted(candidates, key=lambda x: candidates[x], reverse=True):
        found_any = False
        for instruction in instructions:
            if (
                get_manhattan_distance(candidate, instruction["sensor"])
                <= instruction["range"]
            ):
                found_any = True
                break

        if not found_any:
            return candidate[0] * 4000000 + candidate[1]


if __name__ == "__main__":
    instructions = load_instructions()
    grid = Grid(instructions, -1)

    print(find_unknown_beacon(0, 4000000, grid.instructions))

    # ROW = 2000000
    # print(f"Row {ROW} has {grid.check_row()} known tiles.")
