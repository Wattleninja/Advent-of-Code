from collections import Counter
from itertools import combinations


def main():
    with open('02.in') as f:
        data = [line.strip() for line in f]

    twos = threes = 0
    for item in data:
        counts = set(Counter(item).values())
        twos += 2 in counts
        threes += 3 in counts

    print(twos * threes)

    result = ''
    for first, second in combinations(data, 2):
        s = ''
        for c1, c2 in zip(first, second):
            if c1 == c2:
                s += c1
        if len(s) > len(result):
            result = s

    print(result)


if __name__ == '__main__':
    main()
