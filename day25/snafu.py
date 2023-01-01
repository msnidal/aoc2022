SNAFU_LOOKUP = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
BASE10_LOOKUP = {value: key for key, value in SNAFU_LOOKUP.items()}


def load_numbers(filename):
    total = 0
    with open(filename) as file:
        for line in file.readlines():
            total += snafu_to_base10(
                [SNAFU_LOOKUP[character] for character in line.strip()]
            )

    return total


def test_conversion(filename):
    with open(filename) as file:
        for line in file.readlines()[1:]:
            stripped = line.strip().split(" ")
            base10, snafu = stripped[0], stripped[-1]
            assert (
                base10_to_snafu(int(base10)) == snafu
            ), f"Failed to convert {base10} to {snafu}"
            assert snafu_to_base10(
                [SNAFU_LOOKUP[character] for character in snafu]
            ) == int(base10), f"Failed to convert {snafu} to {base10}"


def snafu_to_base10(snafu):
    return sum(digit * 5**i for i, digit in enumerate(reversed(snafu)))


def base10_to_snafu(base10):
    digits, bound = 0, 1
    while base10 >= bound:
        bound += 2 * (5**digits)
        digits += 1

    low = bound - (2 * (5 ** (digits - 1)))
    first_digit = ((base10 - low) // (5 ** (digits - 1))) + 1
    remainder = base10 - ((5 ** (digits - 1)) * first_digit)
    output = [first_digit]

    for digit in reversed(range(digits - 1)):
        options = [(value * (5**digit), value) for value in range(-2, 3)]
        _, value = min(options, key=lambda x: abs(x[0] - remainder))

        output.append(value)
        remainder -= (5**digit) * output[-1]

    return "".join([BASE10_LOOKUP[snafu] for snafu in output])


if __name__ == "__main__":
    test_conversion("day25/test.txt")

    total = load_numbers("day25/input.txt")
    snafu_total = base10_to_snafu(total)
    print(snafu_total)
