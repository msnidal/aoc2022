import string


def load_inputs():
    inputs = []

    with open("day3/input.txt", "r") as f:
        for line in f:
            raw_input = line.strip()
            demarcator = len(raw_input) // 2

            inputs.append((raw_input[:demarcator], raw_input[demarcator:]))

    return inputs


def get_intersection(first: str, second: str) -> str:
    first = set(first)
    second = set(second)

    # THere's always only one
    return first.intersection(second).pop()


def score_letter(letter: str) -> int:
    if letter in string.ascii_lowercase:
        return string.ascii_lowercase.index(letter) + 1
    else:
        return string.ascii_uppercase.index(letter) + len(string.ascii_lowercase) + 1


if __name__ == "__main__":
    inputs = load_inputs()
    missing_score = 0
    badge_score = 0

    group_badges = set()

    for index, (first, second) in enumerate(inputs):
        common = get_intersection(first, second)
        missing_score += score_letter(common)

        badge_set = {character for character in first + second}
        if index % 3 == 0:
            group_badges = badge_set
        else:
            group_badges = group_badges.intersection(badge_set)

        if index % 3 == 2:
            badge = group_badges.pop()
            badge_score += score_letter(badge)

    print(f"Missing score: {missing_score}\nBadge score: {badge_score}")
