import re
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y', 'dx', 'dy'])


def find_smallest_size(points, start=10000, end=15000):
    results = []
    for i in range(start, end):
        min_x = min(p.x + p.dx * i for p in points)
        max_x = max(p.x + p.dx * i for p in points)
        min_y = min(p.y + p.dy * i for p in points)
        max_y = max(p.y + p.dy * i for p in points)

        results.append((max_x, min_x, max_y, min_y, i))

    return min(results, key=lambda t: (t[0] - t[1]) * (t[2] - t[3]))


def main():
    points = []
    with open('inputs/10.in') as f:
        for line in f:
            points.append(Point(*map(int, re.findall(r'-?\d+', line.strip()))))

    max_x, min_x, max_y, min_y, i = find_smallest_size(points)
    lst = [[' '] * (max_x - min_x + 1) for j in range(max_y - min_y + 1)]

    for p in points:
        lst[p.y + p.dy * i - min_y][p.x + p.dx * i - min_x] = '#'

    print('\n'.join(''.join(row) for row in lst))
    print(i)


if __name__ == '__main__':
    main()
