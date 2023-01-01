BLOOD_BLACK_NOTHINGNESS = "."
CELLS = "#"
SAND = "+"

FILENAME = "day14/input.txt"


def parse_instruction(instruction_line):
    grid_sequences = []

    instructions = instruction_line.split(" -> ")
    for instruction in instructions:
        x, y = instruction.split(",")
        grid_sequences.append((int(x), int(y)))

    return grid_sequences


def load_input():
    sequences = []
    with open(FILENAME) as file:
        for line in file:
            instruction = line.strip()
            sequences.append(parse_instruction(instruction))

    return sequences


def show_grid(
    grid, message="Dreadfully distinct against the dark background, you see:"
):
    print(message)
    for row in grid:
        print("".join(row))
    print()


def populate_grid(sequences, include_floor=False, x_buffer=0):
    # Normalize to make it easier to draw
    x_upper_bound = max(
        coordinate[0] for sequence in sequences for coordinate in sequence
    )
    x_lower_bound = min(
        coordinate[0] for sequence in sequences for coordinate in sequence
    )
    y_upper_bound = max(
        coordinate[1] for sequence in sequences for coordinate in sequence
    )

    x_lower_bound -= x_buffer
    x_upper_bound += x_buffer
    # Y lower bound is zero, where sand falls out

    grid = [
        [BLOOD_BLACK_NOTHINGNESS for _ in range(x_lower_bound, x_upper_bound + 1)]
        for _ in range(y_upper_bound + 1)
    ]

    for sequence in sequences:
        prior_coordinates = None

        for coordinates in sequence:
            x, y = coordinates
            x -= x_lower_bound

            grid[y][x] = CELLS

            if prior_coordinates:
                prior_x, prior_y = prior_coordinates
                prior_x -= x_lower_bound

                # Straight lines only
                if prior_x == x:
                    direction = -1 if prior_y > y else 1
                    for y_interlinked in range(prior_y, y + direction, direction):
                        grid[y_interlinked][x] = CELLS
                elif prior_y == y:
                    direction = -1 if prior_x > x else 1
                    for x_interlinked in range(prior_x, x + direction, direction):
                        grid[y][x_interlinked] = CELLS

            prior_coordinates = coordinates

    if include_floor:
        for row in (BLOOD_BLACK_NOTHINGNESS, CELLS):
            grid.append([row for _ in range(x_lower_bound, x_upper_bound + 1)])

    return grid, x_lower_bound


def place_sand(grid, sandspawn):
    """Side effect: places sand in the grid
    Returns false if the sand can't be placed (fell off)
    """

    coordinates = (0, sandspawn)

    while True:
        # Fall off
        try:
            if coordinates[0] + 1 >= len(grid):
                return False
            # First, try down
            elif grid[coordinates[0] + 1][coordinates[1]] == BLOOD_BLACK_NOTHINGNESS:
                coordinates = (coordinates[0] + 1, coordinates[1])
            # Then, try left
            elif coordinates[1] - 1 < 0:
                return False  # Fell off leftwise
            elif (
                grid[coordinates[0] + 1][coordinates[1] - 1] == BLOOD_BLACK_NOTHINGNESS
            ):
                coordinates = (coordinates[0] + 1, coordinates[1] - 1)
            # Then, try right
            elif coordinates[1] > len(grid[0]):
                return False  # Fell off rightwise
            elif (
                grid[coordinates[0] + 1][coordinates[1] + 1] == BLOOD_BLACK_NOTHINGNESS
            ):
                coordinates = (coordinates[0] + 1, coordinates[1] + 1)
            else:
                grid[coordinates[0]][coordinates[1]] = SAND
                return True  # Settled
        except Exception as e:
            breakpoint()
            print("Gootbye")


def flow_sand(grid, x_lower_bound):
    """Keep flowing that sand baby"""

    sand_spawn = 500 - x_lower_bound

    can_place = True
    sand_count = 0
    while can_place:
        can_place = place_sand(grid, sand_spawn)
        # show_grid(grid)
        if can_place:
            sand_count += 1

        if grid[0][sand_spawn] == SAND:
            break

    return sand_count


if __name__ == "__main__":
    sequences = load_input()
    grid, x_lower_bound = populate_grid(sequences, include_floor=True, x_buffer=200)
    show_grid(grid)

    count = flow_sand(grid, x_lower_bound)
    print(count)
