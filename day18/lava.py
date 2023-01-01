import itertools


FILENAME = "day18/input.txt"


def load_droplets(filename):
    voxels = set()
    with open(filename) as file:
        for line in file.readlines():
            x, y, z = line.strip().split(",")
            voxels.add((int(x), int(y), int(z)))

    return voxels


def is_adjacent(voxel, voxels):
    for dimension in range(3):
        for side in (-1, 1):
            check_coordinate = [
                coordinate + side if index == dimension else coordinate
                for index, coordinate in enumerate(voxel)
            ]
            if tuple(check_coordinate) in voxels:
                return True

    return False


def get_exclusions(voxels):
    # Establish a cubic boundary
    bounds = {
        dimension: (
            min(coordinate[dimension] for coordinate in voxels) - 1,
            max(coordinate[dimension] for coordinate in voxels) + 1,
        )
        for dimension in range(3)
    }

    coordinate_grid = dict()  # True if exposed (starting with boundary), False if not
    for x in range(bounds[0][0], bounds[0][1]):
        for y in range(bounds[1][0], bounds[1][1]):
            for z in range(bounds[2][0], bounds[2][1]):
                coordinate_grid[(x, y, z)] = (
                    x in bounds[0] or y in bounds[1] or z in bounds[2]
                )

    new_additions = True
    while new_additions:
        new_additions = False
        for voxel in {
            voxel for voxel, exposed in coordinate_grid.items() if not exposed
        }:
            if is_adjacent(
                voxel,
                {voxel for voxel, exposed in coordinate_grid.items() if exposed}
                - voxels,
            ):
                new_additions = True
                coordinate_grid[voxel] = True

    # Evaluate all voxels inside boundary for adjacency to
    return {voxel for voxel in coordinate_grid if not coordinate_grid[voxel]} - voxels


def count_sides(voxels, exclusions=None):
    if not exclusions:
        exclusions = set()

    total_exposed_sides = 0

    for voxel in voxels:
        exposed_sides = 6
        for dimension in range(3):
            for side in (-1, 1):
                check_coordinate = [
                    coordinate + side if index == dimension else coordinate
                    for index, coordinate in enumerate(voxel)
                ]

                coordinate_tuple = tuple(check_coordinate)
                if coordinate_tuple in voxels or coordinate_tuple in exclusions:
                    exposed_sides -= 1

        total_exposed_sides += exposed_sides

    return total_exposed_sides


if __name__ == "__main__":
    voxels = load_droplets(FILENAME)
    exclusions = get_exclusions(voxels)
    sides = count_sides(voxels, exclusions)

    print(sides)
