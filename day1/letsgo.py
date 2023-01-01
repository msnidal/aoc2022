def load_data():
    with open("day1/input.txt") as f:
        return [line.strip() for line in f.readlines()]


if __name__ == "__main__":
    lines = load_data()

    packs = []
    pack = 0

    for line in lines:
        if line == "":
            packs.append(pack)
            pack = 0
        else:
            pack += int(line)

    greatest = max(packs)
    sorted_greatest = sorted(packs)
    breakpoint()
    print(greatest)
