FILENAME = "day13/input.txt"


def apply_buffer(buffer, pointer_stack):
    if buffer:
        number = int("".join(buffer))
        buffer = []
        pointer_stack[-1].append(number)
    return buffer


def parse_packet(packet):
    items = []
    item = []

    pointer_stack = [item]
    number_buffer = []

    for character in packet:
        if character == ",":
            number_buffer = apply_buffer(number_buffer, pointer_stack)
            if len(pointer_stack) == 1:
                items.append(item[0])
                item = []
                pointer_stack = [item]

        elif character == "[":
            new_item = []

            pointer_stack[-1].append(new_item)
            pointer_stack.append(new_item)

        elif character == "]":
            number_buffer = apply_buffer(number_buffer, pointer_stack)
            pointer_stack.pop()

        else:
            number_buffer.append(character)

    apply_buffer(number_buffer, pointer_stack)
    if item:
        items.append(item[0])

    assert f"[{packet}]" == render_packet(
        items
    ), f"Failed to parse {'[' + packet + ']'}\n{render_packet(items)}"

    return items


def render_packet(packet):
    rendered = "["
    for index, item in enumerate(packet):
        if type(item) == int:
            rendered += str(item)
        elif type(item) == list:
            rendered += render_packet(item)

        if index < len(packet) - 1:
            rendered += ","

    return rendered + "]"


def load_input(paired=True):
    packets = []
    with open(FILENAME) as file:
        packet = {}
        for index, line in enumerate(file):
            stripped = line.strip()
            if stripped:
                parsed = parse_packet(stripped[1:-1])

                if paired:
                    if "left" in packet:
                        packet["right"] = parsed
                    else:
                        packet["left"] = parsed
                else:
                    packets.append(parsed)
            else:
                if paired:
                    packets.append(packet)
                    packet = {}

        if paired:
            packets.append(packet)
        else:
            packets += [[[2]]] + [[[6]]]

    return packets


def print_depth(message, depth):
    print(f"{'  ' * depth}- {message}")


def compare_values(left, right, depth=0):
    print_depth(f"Comparing {left} to {right}", depth)

    if type(left) == int and type(right) == int:
        if left < right:
            print_depth(
                "Left side is smaller, so inputs are in the right order", depth + 1
            )
            return True
        elif left > right:
            print_depth(
                "Right side is smaller, so inputs are in the wrong order", depth + 1
            )
            return False
    elif type(left) == list and type(right) == list:
        for index, datum in enumerate(left):
            if index >= len(right):
                print_depth(
                    "Right side ran out of items, so inputs are in the wrong order",
                    depth + 1,
                )
                return False
            else:
                returned = compare_values(datum, right[index], depth + 1)
                if returned is not None:
                    return returned
        if len(left) < len(right):
            print_depth(
                "Left side ran out of items, so inputs are in the right order",
                depth + 1,
            )
            return True
    elif type(left) == int and type(right) == list:
        left = [left]
        decision = compare_values(left, right, depth + 1)
        if decision is not None:
            return decision
    elif type(left) == list and type(right) == int:
        right = [right]
        decision = compare_values(left, right, depth + 1)
        if decision is not None:
            return decision


def part_one(packets):
    packets = load_input()

    result = 0
    for index, packet in enumerate(packets):
        print(render_packet(packet["left"]))
        print(f"== Pair {index + 1} ==")
        result += compare_values(packet["left"], packet["right"])
        print()

    print(result)


class BinaryNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.count = 1

    def __repr__(self):
        return f"BinaryNode({self.value})"

    def insert(self, value):
        compare = compare_values(self.value, value)
        if compare is False:
            if self.left is None:
                self.left = BinaryNode(value)
            else:
                self.left.insert(value)
        elif compare is True:
            if self.right is None:
                self.right = BinaryNode(value)
            else:
                self.right.insert(value)
        else:
            self.count += 1

    def to_list(self):
        result = []
        if self.left is not None:
            result += self.left.to_list()
        result += [self.value] * self.count
        if self.right is not None:
            result += self.right.to_list()
        return result


def part_two(packets):
    tree = BinaryNode(packets[0])

    for packet in packets[1:]:
        tree.insert(packet)

    listified = tree.to_list()
    multiple = 1
    for search in ([[2]], [[6]]):
        multiple *= listified.index(search) + 1

    print(listified)
    print(multiple)


if __name__ == "__main__":
    packets = load_input(paired=False)
    # part_one(packets)
    part_two(packets)
