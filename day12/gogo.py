import string
import math

from colorama import Fore, Style

FILENAME = "day12/input.txt"


class Tile:
    def __init__(self, value, row, column):
        self.value = value
        self.row = row
        self.column = column

    def __repr__(self):
        return f"Tile({self.value}, {self.row}, {self.column})"

    def __str__(self):
        return f"Tile {self.value} at ({self.row}, {self.column})"

    def can_travel(self, other):
        return other.value <= self.value + 1

    def get_adjacent_indices(self, row_length, column_length):
        candidates = [
            (self.row - 1, self.column),
            (self.row + 1, self.column),
            (self.row, self.column - 1),
            (self.row, self.column + 1),
        ]
        selector = [
            candidate
            for candidate in candidates
            if candidate[0] >= 0
            and candidate[1] >= 0
            and candidate[0] < row_length
            and candidate[1] < column_length
        ]

        return selector

    def score(self, other):
        return math.sqrt(
            (self.row - other.row) ** 2 + (self.column - other.column) ** 2
        ) + abs(self.value - other.value)


def show_grid(grid, path=None):
    for row in grid:
        for column in row:
            character = string.ascii_lowercase[column.value]
            if path and (column.row, column.column) in path:
                print(f"{Fore.GREEN}{character}{Style.RESET_ALL}", end="")
            else:
                print(f"{character}", end="")
        print()


def load_input():
    begin, end = None, None
    grid = []

    with open(FILENAME, "r") as f:
        for row_index, line in enumerate(f.readlines()):
            row = []
            stripped = line.strip()
            for character_index, character in enumerate(stripped):
                if character == "S":
                    height = 0
                    begin = (row_index, character_index)
                elif character == "E":
                    height = 25
                    end = (row_index, character_index)
                else:
                    height = string.ascii_lowercase.index(character)

                row.append(Tile(height, row_index, character_index))
            grid.append(row)

    return grid, begin, end


def get_all_lowlands(grid):
    lowlands = []
    for row in grid:
        for tile in row:
            if tile.value == 0:
                lowlands.append((tile.row, tile.column))
    return lowlands


def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return total_path


def find_path(grid, begin, end):
    """Semi-shoddy implementation of an A* algorithm"""

    open_set = [begin]
    came_from, g_score, f_score = {}, {}, {}

    for row in grid:
        for tile in row:
            g_score[(tile.row, tile.column)] = math.inf
            f_score[(tile.row, tile.column)] = math.inf

    g_score[begin] = 0
    f_score[begin] = grid[begin[0]][begin[1]].score(grid[end[0]][end[1]])

    while open_set:
        current = min(open_set, key=lambda position: f_score[position])
        # show_grid(grid, reconstruct_path(came_from, current))
        if current == end:
            return reconstruct_path(came_from, current)

        open_set.remove(current)

        for neighbor in grid[current[0]][current[1]].get_adjacent_indices(
            len(grid), len(grid[0])
        ):
            if not grid[current[0]][current[1]].can_travel(
                grid[neighbor[0]][neighbor[1]]
            ):
                continue

            tentative_g_score = g_score[current] + grid[current[0]][current[1]].score(
                grid[neighbor[0]][neighbor[1]]
            )

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + grid[neighbor[0]][
                    neighbor[1]
                ].score(grid[end[0]][end[1]])
                if neighbor not in open_set:
                    open_set.append(neighbor)


if __name__ == "__main__":
    grid, begin, end = load_input()
    lowlands = get_all_lowlands(grid)

    lowest_global = None
    for lowland in lowlands:
        path = find_path(grid, lowland, end)

        if path and (lowest_global is None or len(path) < len(lowest_global)):
            show_grid(grid, path)
            print(f"Path length: {len(path) - 1}")
            lowest_global = path
