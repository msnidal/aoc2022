ROCK = "rock"
PAPER = "paper"
SCISSORS = "scissors"
PLAYER = "player"
OPPONENT = "opponent"
LOSE = "lose"
WIN = "win"
TIE = "tie"

DECODER = {
    "A": (OPPONENT, ROCK),
    "B": (OPPONENT, PAPER),
    "C": (OPPONENT, SCISSORS),
    "X": (PLAYER, LOSE),
    "Y": (PLAYER, TIE),
    "Z": (PLAYER, WIN),
}

SAMPLE = "sample.txt"
INPUTS = "day2.txt"


def score_outcome(moves: tuple[(str, str), (str, str)]) -> int:
    score = 0

    if moves[1][1] == LOSE:
        if moves[0][1] == ROCK:
            score += 3
        elif moves[0][1] == PAPER:
            score += 1
        elif moves[0][1] == SCISSORS:
            score += 2
    elif moves[1][1] == TIE:
        score += 3
        if moves[0][1] == ROCK:
            score += 1
        elif moves[0][1] == PAPER:
            score += 2
        elif moves[0][1] == SCISSORS:
            score += 3
    elif moves[1][1] == WIN:
        score += 6
        if moves[0][1] == ROCK:
            score += 2
        elif moves[0][1] == PAPER:
            score += 3
        elif moves[0][1] == SCISSORS:
            score += 1

    return score


def score(moves: tuple[(str, str), (str, str)]) -> int:
    score = 0

    if moves[1][1] == ROCK:
        score += 1  # Free point for rock

        if moves[0][1] == SCISSORS:
            score += 6
        elif moves[0][1] == ROCK:  # Tie
            score += 3
    elif moves[1][1] == PAPER:
        score += 2

        if moves[0][1] == ROCK:
            score += 6
        elif moves[0][1] == PAPER:  # Tie
            score += 3
    elif moves[1][1] == SCISSORS:
        score += 3

        if moves[0][1] == PAPER:
            score += 6
        elif moves[0][1] == SCISSORS:
            score += 3

    return score


def load_games():
    games = []
    with open(INPUTS) as f:
        for line in f:
            raw_moves = line.strip().split(" ")
            moves = (DECODER[raw_moves[0]], DECODER[raw_moves[1]])
            games.append(moves)

    return games


if __name__ == "__main__":
    games = load_games()

    game_score = 0
    for game in games:
        game_score += score_outcome(game)

    print(game_score)
