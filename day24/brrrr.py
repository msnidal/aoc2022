import math

BLIZZARDS = ("^", ">", "v", "<")


def load_blizzard(filename):
    """Width and height are inclusive of the outer walls. Looping occurs one level inwards"""
    blizzards = dict()

    with open(filename) as file:
        for y, line in enumerate(file.readlines()):
            for x, character in enumerate(line.strip()):
                if character in BLIZZARDS:
                    blizzards[(x, y)] = [
                        BLIZZARDS.index(character)
                    ]  # Coordinate basis using inner width/height

    return blizzards, (x + 1, y + 1)


def show_valley(blizzards, party, width, height, start, end):
    print("Brrrr.....")
    for y in range(height):
        for x in range(width):
            if (x == 0 or x == width - 1 or y == 0 or y == height - 1) and (
                x,
                y,
            ) not in (start, end):
                print("#", end="")
            elif (x, y) in blizzards:
                blizzard = blizzards[(x, y)]
                if len(blizzard) > 1:
                    print("2", end="")
                else:
                    print(BLIZZARDS[blizzard[0]], end="")
            elif (x, y) == party:
                print("E", end="")
            else:
                print(".", end="")
        print()


def tick(blizzards, width, height):
    inner_width, inner_height = width - 2, height - 2
    new_blizzards = dict()

    for tile in blizzards:
        for blizzard in blizzards[tile]:
            direction = BLIZZARDS[blizzard]
            if direction == "^":
                new_tile = (tile[0], (((tile[1] - 1) - 1) % inner_height) + 1)
            elif direction == ">":
                new_tile = ((((tile[0] + 1) - 1) % inner_width) + 1, tile[1])
            elif direction == "v":
                new_tile = (tile[0], (((tile[1] + 1) - 1) % inner_height) + 1)
            elif direction == "<":
                new_tile = ((((tile[0] - 1) - 1) % inner_width) + 1, tile[1])

            new_blizzards[new_tile] = new_blizzards.get(new_tile, []) + [blizzard]

    return new_blizzards


def heuristic(party, end, steps):
    """Return the manhattan distance between the party and the exit
    Also including the total steps to add a wait cost
    """
    return abs(party[0] - end[0]) + abs(party[1] - end[1]) + steps


def get_moves(party, exit, width, height):
    """Get all the available moves from the current position"""
    moves = [party]  # Waiting is allowed

    # Check all the adjacent tiles
    for (x, y) in [
        (party[0] + 1, party[1]),
        (party[0] - 1, party[1]),
        (party[0], party[1] + 1),
        (party[0], party[1] - 1),
    ]:
        if x > 0 and x < width - 1 and y > 0 and y < height - 1:
            moves.append((x, y))
        elif (x, y) == exit:
            moves.append((x, y))

    return moves


def search(blizzards, time, party, exit, width, height):
    potential_moves = get_moves(party, exit, width, height)
    if exit in potential_moves:
        return time + 1

    next_blizzard = blizzards[(time + 1) % len(blizzards)]
    scored_moves = [
        (heuristic(move, exit, time + 1), move)
        for move in potential_moves
        if move not in next_blizzard
    ]

    for _, move in sorted(scored_moves, key=lambda x: x[0]):
        path = search(blizzards, time + 1, move, exit, width, height)
        if path:
            return path

    return None


if __name__ == "__main__":
    blizzards, (width, height) = load_blizzard("day24/sample.txt")
    start, exit = (1, 0), (width - 2, height - 1)
    blizzards = [blizzards]

    # There are only so many unique blizzard positions. Caching everything in memory lets us iterate pathfinding quickly
    for i in range(math.lcm(width - 2, height - 2) - 1):
        blizzards.append(tick(blizzards[-1], width, height))

    path = search(blizzards, 0, start, exit, width, height)
    print(path)
