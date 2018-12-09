from collections import defaultdict


def main():
    with open('inputs/03.in') as f:
        overlaps = defaultdict(int)
        claims = defaultdict(list)

        for line in f:
            id_, _, offsets, dim = line.strip()[1:].split()
            x, y = map(int, offsets[:-1].split(','))
            w, h = map(int, dim.split('x'))

            for i in range(x, x + w):
                for j in range(y, y + h):
                    v = (i, j)
                    claims[id_].append(v)
                    overlaps[v] += 1

    print(sum(1 for count in overlaps.values() if count >= 2))
    for claim_id, claim_list in claims.items():
        if all(overlaps[claim] == 1 for claim in claim_list):
            print(claim_id)
            break


if __name__ == '__main__':
    main()
