from collections import deque


def main():
    mapping = {}
    with open('inputs/12.in') as f:
        _, initial = next(f).strip().split(': ')
        for line in f:
            line = line.strip()
            if line:
                from_, to = line.split(' => ')
                mapping[from_] = to

    initial = f'...{initial}...'
    # print(f'{0:>3}: {initial}')
    generation = list(initial)
    prev_gen = initial
    pot_zero = initial.find('#')
    prev = 0
    diffs = deque(maxlen=5)
    for i in range(1, 50_000_000_000 + 1):
        for pot in range(2, len(prev_gen) - 2):
            group = prev_gen[pot - 2:pot + 3]
            generation[pot] = mapping.get(group, '.')
        if '#' in generation[-5:]:
            generation.extend('...')

        prev_gen = ''.join(generation)
        # print(f'{i:>3}: {prev_gen}')
        pot_sum = sum(i for i, c in enumerate(prev_gen, start=-pot_zero) if c == '#')
        diff = pot_sum - prev
        diffs.append(diff)
        if len(diffs) > 1 and all(x == diff for x in diffs):
            break
        prev = pot_sum

    print(pot_sum)
    print((50_000_000_000 - i) * diff + pot_sum)


if __name__ == '__main__':
    main()
