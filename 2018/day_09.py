from collections import deque
from itertools import cycle


def get_winning_score(num_players, max_points):
    scores = [0] * num_players
    marbles = deque([0], maxlen=max_points + 1)
    players = cycle(range(num_players))

    for i in range(1, marbles.maxlen):
        current_player = next(players)
        if i % 23 == 0:
            marbles.rotate(7)
            marble = marbles.pop()
            marbles.rotate(-1)
            scores[current_player] += marble + i
        else:
            marbles.rotate(-1)
            marbles.append(i)

    print(max(scores))


def main():
    with open('inputs/09.in') as f:
        parts = f.read().strip().split()
        num_players, max_points = int(parts[0]), int(parts[-2])

    get_winning_score(num_players, max_points)
    get_winning_score(num_players, max_points * 100)


if __name__ == '__main__':
    main()
