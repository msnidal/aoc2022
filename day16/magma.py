from functools import cache
import parse

VARIATIONS = (
    "Valve {valve_name} has flow rate={flow_rate}; tunnels lead to valves {connected_valves}",
    "Valve {valve_name} has flow rate={flow_rate}; tunnel leads to valve {connected_valves}",
)


class Map:
    def __init__(self, filename, time_limit=30, agents=1):
        self.valves = {}
        with open(filename) as file:
            instructions = file.read().splitlines()

            for instruction in instructions:
                for variation in VARIATIONS:
                    results = parse.parse(variation, instruction)

                    if results:
                        break

                self.valves[results["valve_name"]] = {
                    "flow_rate": int(results["flow_rate"]),
                    "connections": results["connected_valves"].split(", "),
                }
        self.get_path_length_cache = (
            {}
        )  # Would use functools cache but using a set in recursion (unhashable)
        self.time_limit = time_limit
        self.agents = agents

    def get_path_length(self, starting_valve, destination_valve, travelled_valves=None):
        """Return the number of minutes required to reach the destination valve"""

        if travelled_valves is None:
            travelled_valves = set()
        else:
            travelled_valves = travelled_valves.copy()

        if starting_valve == destination_valve:
            return 0

        travelled_valves.add(starting_valve)

        paths = []
        for valve in self.valves[starting_valve]["connections"]:
            if valve not in travelled_valves:
                path_length = self.get_path_length(
                    valve, destination_valve, travelled_valves
                )
                if path_length is not None:
                    paths.append(path_length + 1)

        if paths:
            return min(paths)
        return None

    def find_move(self, current_valve, opened_valves=None, time=1):
        """Iterate recursively through all possible chains of moves, determining and returning the potential score of the entire sequence of moves"""

        if time > self.time_limit:
            return None, opened_valves

        if opened_valves is None:
            opened_valves = {}
        else:
            opened_valves = (
                opened_valves.copy()
            )  # Allow for recursion without affecting the original set
            opened_valves[current_valve] = time, self.valves[current_valve][
                "flow_rate"
            ] * (self.time_limit - time)
            time += 1

        remaining_time = (
            self.time_limit - time
        )  # Applicable to both opening (kicks in next minute) and moving (advance time)

        potential_move_scores = {}

        # Check all possible moves, including the current one if it is not already open
        for valve in self.valves:
            # If the valve is not already open, add it to the potential moves
            if valve not in opened_valves and self.valves[valve]["flow_rate"] > 0:

                if current_valve + valve in self.get_path_length_cache:
                    path_length = self.get_path_length_cache[current_valve + valve]
                else:
                    path_length = self.get_path_length(current_valve, valve)
                    self.get_path_length_cache[current_valve + valve] = path_length

                if path_length is not None and remaining_time - path_length >= 0:
                    score_this_move = self.valves[valve]["flow_rate"] * (
                        remaining_time - path_length
                    )
                    next_scores, path_opened_valves = self.find_move(
                        valve, opened_valves, time + path_length
                    )

                    if next_scores is not None:
                        score_this_move += next_scores

                    potential_move_scores[valve] = {
                        "score": score_this_move,
                        "opened_valves": path_opened_valves,
                    }

        if potential_move_scores:
            sorted_moves = sorted(
                potential_move_scores.items(),
                key=lambda item: item[1]["score"],
                reverse=True,
            )
            return sorted_moves[0][1]["score"], sorted_moves[0][1]["opened_valves"]

        return None, opened_valves


if __name__ == "__main__":
    map = Map("sample.txt")
    starting_valve = "AA"

    move = map.find_move(starting_valve)
    print(move)
