LS = "ls"
CD = "cd"


def load_file(filename):
    with open(filename) as f:
        lines = f.read().splitlines()

    commands = []
    command = {}

    for line in lines:
        if line[0] == "$":
            if command:
                commands.append(command)
                command = {}

            command["operation"] = line[2:4]
            if line[2:4] == CD:
                command["argument"] = line[5:]

            command["output"] = []
        else:
            size, file = tuple(line.split(" "))
            if size == "dir":
                size = "0"

            command["output"].append(
                {
                    "size": int(size),
                    "file": file,
                    "type": "dir" if size == "0" else "file",
                }
            )

    if command:
        commands.append(command)

    return commands


class Directory:
    def __init__(self, name, parent=None, depth=0):
        self.name = name
        self.parent = parent
        self.depth = depth
        self.size = None
        self.children = {}

    def add_child(self, child):
        self.children[child.name] = child

    def __repr__(self):
        predent = " " * self.depth + "-"
        children = [str(child) for child in self.children.values()]
        children_string = "\n".join(children)
        return f"{predent} Directory({self.name}, {self.size}):\n{children_string}"


class File:
    def __init__(self, name, size, depth=0):
        self.name = name
        self.size = size
        self.depth = depth

    def __repr__(self):
        predent = " " * self.depth + "-"
        return f"{predent} File({self.name}, {self.size})"


def populate(commands):
    home = Directory("/")
    cursor = home
    depth = 0

    for command in commands:
        if command["operation"] == LS:
            for file in command["output"]:
                if file["type"] == "dir":
                    directory = Directory(file["file"], parent=cursor, depth=depth)
                    cursor.add_child(directory)
                else:
                    file = File(file["file"], file["size"], depth=depth)
                    cursor.add_child(file)
        elif command["operation"] == CD:
            if command["argument"] == "..":
                cursor = cursor.parent
                depth -= 1
            elif command["argument"] == "/":
                cursor = home
                depth = 0
            else:
                cursor = cursor.children[command["argument"]]
                depth += 1

    return home


def solve(home):
    """Use a depth-first search to find the size of each directory, including recursively. Return the sum of all directories with a size less than 100000"""

    def depth_first_search(node):
        if isinstance(node, File):
            return node.size

        size = 0
        for child in node.children.values():
            size += depth_first_search(child)

        node.size = size
        return size

    depth_first_search(home)

    def find_smallest_directory(node, target, candidates):
        if isinstance(node, File):
            return
        elif node.size >= target:
            candidates.append(node)

        for child in node.children.values():
            find_smallest_directory(child, target, candidates)

    # Part 1
    """
    def find_small_directories(node, payload):
        if isinstance(node, File):
            return
        elif node.size <= 100000:
            payload.append((node.name, node.size))

        for child in node.children.values():
            find_small_directories(child, payload)
        
    treasure = []
    find_small_directories(home, treasure)
    print(treasure)

    total = 0
    for loot in treasure:
        total += loot[1]
    
    #return total
    """

    # Part 2
    available = 70000000 - home.size
    desired = 30000000
    target = desired - available

    print(f"Available: {available} Desired: {desired} Target: {target}")

    candidates = []
    find_smallest_directory(home, target, candidates)

    smallest = min(candidates, key=lambda x: x.size)
    print(smallest)
    return smallest.size


if __name__ == "__main__":
    output = load_file("day7/input.txt")
    home = populate(output)
    total = solve(home)
    print(home)
    print(total)
