from collections import defaultdict, namedtuple

Point = namedtuple('Point', ['x', 'y'])


def manhattan(p1: Point, p2: Point):
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


def main():
    with open('06.in') as f:
        data = [Point(*map(int, line.split(', '))) for line in f]

    width = max(p.x for p in data)
    height = max(p.y for p in data)
    infinite = set()
    safe_distance = 10000
    safe_region_size = 0

    areas = defaultdict(int)

    for i in range(width + 1):
        for j in range(height + 1):
            dists = [(p, manhattan(p, Point(i, j))) for p in data]
            closest, dist = min(dists, key=lambda item: item[1])

            if len([d for p, d in dists if d == dist]) == 1:
                areas[closest] += 1

                if 0 in (i, j) or i == width or j == height:
                    infinite.add(closest)

            safe_region_size += sum(d for p, d in dists) < safe_distance

    print(max(area for point, area in areas.items() if point not in infinite))
    print(safe_region_size)


if __name__ == '__main__':
    main()
