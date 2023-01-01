FILENAME = "day10/input.txt"
NOOP = "noop"
ADDX = "addx"


def parse_signal(signal):
    if ADDX in signal:
        command, argument = signal.split(" ")
    else:
        command, argument = signal, None

    parsed = {"command": command}
    if argument:
        parsed["argument"] = int(argument)

    return parsed


def load_input():
    signals = []
    with open(FILENAME, "r") as file:
        signals = [parse_signal(line.strip()) for line in file.readlines()]

    return signals


class Tube:
    def __init__(self, register=1):
        self.register = register
        self.current_cycle = 0
        self.screen = [[]]
        self.interesting_signals = []

    def __repr__(self):
        return "\n".join(["".join(line) for line in self.screen])
        # return f"Tube(X:{self.register}, C:{self.current_cycle})"

    def is_interesting_cycle(self):
        is_interesting = (self.current_cycle - 20) % 40 == 0

        return is_interesting

    def get_interesting_signal_strength(self):
        output = 0
        for signal in self.interesting_signals:
            if signal["cycle"] <= 220:
                output += signal["register"] * signal["cycle"]

        return output

    def has_pixel(self):
        return self.current_cycle % 40 in {
            self.register - 1,
            self.register,
            self.register + 1,
        }

    def draw_screen(self):
        self.screen[-1].append("#" if self.has_pixel() else ".")
        if (self.current_cycle + 1) % 40 == 0:
            self.screen.append([])

    def cycle(self):
        self.draw_screen()
        self.current_cycle += 1

        if self.is_interesting_cycle():
            self.interesting_signals.append(
                {"register": self.register, "cycle": self.current_cycle}
            )

    def run_command(self, signal):
        if signal["command"] == ADDX:
            for _ in range(2):
                self.cycle()
            self.register += signal["argument"]
        elif signal["command"] == NOOP:
            self.cycle()


if __name__ == "__main__":
    signals = load_input()

    tube = Tube()
    for signal in signals:
        tube.run_command(signal)

    print(tube)
