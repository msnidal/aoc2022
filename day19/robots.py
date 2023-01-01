import parse

FILENAME = "day19/sample.txt"
TEMPLATE = "Blueprint {index:d}: Each ore robot costs {ore_robot_ore_cost:d} ore. Each clay robot costs {clay_robot_ore_cost:d} ore. Each obsidian robot costs {obsidian_robot_ore_cost:d} ore and {obsidian_robot_clay_cost:d} clay. Each geode robot costs {geode_robot_ore_cost:d} ore and {geode_robot_obsidian_cost:d} obsidian."
MATERIALS = {"ore", "clay", "obsidian", "geode"}

MINUTES = 16


def load_costs(filename):
    with open(filename) as file:
        costs = [parse.parse(TEMPLATE, line.strip()) for line in file.readlines()]

    blueprints = []
    for cost in costs:
        blueprint = {"index": cost["index"]}
        for robot_material in MATERIALS:
            blueprint[robot_material] = {}
            for cost_material in MATERIALS:
                if f"{robot_material}_robot_{cost_material}_cost" in cost:
                    robot_cost = cost[f"{robot_material}_robot_{cost_material}_cost"]
                else:
                    robot_cost = 0

                blueprint[robot_material][cost_material] = robot_cost
        blueprints.append(blueprint)

    return blueprints


def get_move(robots, materials, blueprint, minutes_remaining=MINUTES, moves=None):
    if moves is None:
        moves = []

    branches = []

    for robot_material in MATERIALS:
        # We have one build action per turn, so we don't need any more than the max blueprint materials
        if robot_material != "geode":
            materials_needed = max(
                [blueprint[material][robot_material] for material in MATERIALS]
            )
            if robots[robot_material] >= materials_needed:
                continue

        can_build_robot = True
        material_times = {}
        for component_material in MATERIALS:
            if blueprint[robot_material][component_material] == 0:
                continue
            elif robots[component_material] == 0:
                can_build_robot = False
                break

            material_times[component_material] = (
                blueprint[robot_material][component_material]
                - materials[component_material]
            ) // robots[component_material]

        if can_build_robot:
            build_time = max(material_times.values()) + 1

            if build_time > minutes_remaining:
                can_build_robot = False
                break

            # Try to branch on building this
            branch_robots = robots.copy()
            branch_materials = materials.copy()
            branch_moves = moves.copy()

            branch_robots[robot_material] += 1
            branch_materials = {
                material: materials[material] + (robots[material] * build_time)
                for material in MATERIALS
            }
            branch_moves.append((robot_material, minutes_remaining))

            moves, score = get_move(
                branch_robots,
                branch_materials,
                blueprint,
                minutes_remaining - build_time,
                branch_moves,
            )
            branches.append((moves, score))

    if branches:
        return max(branches, key=lambda branch: branch[1])
    else:  # No more robots to build, so just collect materials
        return moves, materials["geode"] + (robots["geode"] * minutes_remaining)


def mine(blueprint):
    print(f"Evaluating blueprint {blueprint['index']}...")
    robots = {material: 1 if material == "ore" else 0 for material in MATERIALS}
    materials = {material: 0 for material in MATERIALS}

    moves, score = get_move(robots, materials, blueprint)
    print(f"Move sequence: {moves}")
    print(f"Best score: {score}")

    return score * blueprint["index"]


if __name__ == "__main__":
    blueprints = load_costs(FILENAME)
    best_scores = [mine(blueprint) for blueprint in blueprints]
    print(sum(best_scores))
