FILE = "day8/input.txt"


def load_forest():
    with open(FILE) as file:
        lines = [line.strip() for line in file.readlines()]

    height = len(lines)
    width = len(lines[0])

    forest = [[] for _ in range(height)]
    for i in range(height):
        for j in range(width):
            forest[i].append(int(lines[i][j]))

    return forest


def get_visibility(forest):
    """Part 1"""
    visible_trees = set()

    for rows_reversed in (False, True):
        for columns_reversed in (False, True):
            maxima = {
                "row": [-1 for _ in range(len(forest))],
                "column": [-1 for _ in range(len(forest[0]))],
            }
            print(
                f"rows_reversed: {rows_reversed}, columns_reversed: {columns_reversed}"
            )

            for row_index in range(len(forest)):
                if rows_reversed:
                    row_index = len(forest) - row_index - 1

                for column_index in range(len(forest[0])):
                    if columns_reversed:
                        column_index = len(forest[0]) - column_index - 1

                    tree_index = column_index * len(forest[0]) + row_index

                    if forest[row_index][column_index] > maxima["row"][row_index]:
                        maxima["row"][row_index] = forest[row_index][column_index]
                        visible_trees.add(tree_index)
                    if forest[row_index][column_index] > maxima["column"][column_index]:
                        maxima["column"][column_index] = forest[row_index][column_index]
                        visible_trees.add(tree_index)

    return visible_trees


def get_best_spot(forest):
    """Part 2"""

    DIRECTIONS = ("N", "E", "S", "W")
    scenic_destination = {"index": -1, "score": -1}

    for row_index, row in enumerate(forest):
        for column_index, column in enumerate(row):
            scores = {direction: 0 for direction in DIRECTIONS}
            home_height = forest[row_index][column_index]
            print(
                f"row_index: {row_index}, column_index: {column_index}: forest[row_index][column_index]: {forest[row_index][column_index]}"
            )
            for direction in DIRECTIONS:
                if direction == "N":
                    iterable = range(row_index - 1, -1, -1)
                elif direction == "E":
                    iterable = range(column_index + 1, len(forest[0]))
                elif direction == "S":
                    iterable = range(row_index + 1, len(forest))
                elif direction == "W":
                    iterable = range(column_index - 1, -1, -1)

                for target_index in iterable:
                    scores[direction] += 1
                    if direction in ("N", "S"):
                        target_row = target_index
                        target_column = column_index
                    else:
                        target_row = row_index
                        target_column = target_index

                    if forest[target_row][target_column] >= home_height:
                        break
            print(scores)

            viewing_distance = 1
            for score in scores.values():
                viewing_distance *= score

            if viewing_distance > scenic_destination["score"]:
                scenic_destination["index"] = (row_index, column_index)
                scenic_destination["score"] = viewing_distance

    return scenic_destination


if __name__ == "__main__":
    forest = load_forest()
    # Part 1:
    # trees = get_visibility(forest)
    # print(trees)
    # print(len(trees))

    # Part 2:
    best_spot = get_best_spot(forest)
    print(best_spot)
