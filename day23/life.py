DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]


def load_elves(filename):
    with open(filename) as file:
        lines = [line.strip() for line in file.readlines()]

    dimension = len(lines[0]) // 2  # (0, 0) in the centre
    elves = {
        (column_index - dimension, row_index - dimension)
        for row_index, line in enumerate(lines)
        for column_index, character in enumerate(line)
        if character == "#"
    }

    return elves


def surrounding_tiles(tile):
    return {
        (x, y): (tile[0] + x, tile[1] + y)
        for x in range(-1, 2)
        for y in range(-1, 2)
        if (x, y) != (0, 0)
    }


def propose_moves(elves, offset=0):
    proposed_moves = {}
    for elf in elves:
        adjacent = surrounding_tiles(elf)
        if len(set(adjacent.values()) & elves) == 0:  # By their lonesome
            continue
        else:
            hits = [
                direction
                for surrounding_tile in adjacent
                if adjacent[surrounding_tile] in elves
                for direction in DIRECTIONS
                if (direction[0] != 0 and direction[0] == surrounding_tile[0])
                or (direction[1] != 0 and direction[1] == surrounding_tile[1])
            ]

            for direction in DIRECTIONS[offset:] + DIRECTIONS[:offset]:
                if not direction in hits:
                    destination = (elf[0] + direction[0], elf[1] + direction[1])
                    if destination in proposed_moves:
                        proposed_moves[destination] = None  # Nobody moves here!
                    else:
                        proposed_moves[destination] = elf
                    break  # One proposed move per turn

    return proposed_moves


def show_elves(elves):
    dimension = max(abs(tile[0]) for tile in elves) + 1
    for y in range(-dimension, dimension + 1):
        for x in range(-dimension, dimension + 1):
            if (x, y) in elves:
                print("#", end="")
            else:
                print(".", end="")
        print()


def get_smallest_rectangle(elves):
    enclosing_rectangle = [
        (func(elf[0] for elf in elves), func(elf[1] for elf in elves))
        for func in (min, max)
    ]

    count = 0
    for row in range(enclosing_rectangle[0][1], enclosing_rectangle[1][1] + 1):
        for column in range(enclosing_rectangle[0][0], enclosing_rectangle[1][0] + 1):
            if (column, row) not in elves:
                count += 1

    return count


if __name__ == "__main__":
    elves = load_elves("day23/input.txt")
    show_elves(elves)

    for move in range(100000):
        moves = propose_moves(elves, move % 4)
        for move in moves:
            if moves[move] is not None:
                elf = moves[move]
                elves.remove(elf)
                elves.add(move)

        # show_elves(elves)
        if not moves:
            print(move + 1)
            break

    # Part 1 just stop after move in range(10)
    # print(get_smallest_rectangle(elves))
