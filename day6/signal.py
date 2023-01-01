def load_signal(filename):
    with open(filename) as f:
        return [line.strip() for line in f]


def process_signal(signal, offset=4):
    for index in range(offset, len(signal)):
        trailing = signal[:index][-offset:]
        characters = {character for character in trailing}

        if len(characters) == offset:
            return index


if __name__ == "__main__":
    signals = load_signal("sample.txt")

    for signal in signals:
        print(process_signal(signal, 14))
