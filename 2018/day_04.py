from collections import defaultdict


def main():
    with open('inputs/04.in') as f:
        data = [line.strip() for line in f]

    guard_sleep = defaultdict(int)
    freq = defaultdict(lambda: defaultdict(int))
    gid = prev = None
    for entry in sorted(data):
        ts, details = entry[1:].split('] ')
        minute = int(ts.split()[1].split(':')[1])

        if details.startswith('Guard'):
            gid = int(details.split()[1][1:])

        elif details == 'wakes up':
            guard_sleep[gid] += minute - prev
            for m in range(prev, minute):
                freq[gid][m] += 1

        elif details == 'falls asleep':
            prev = minute

    best_guard = max(guard_sleep, key=lambda k: guard_sleep[k])
    most_asleep = max(freq[best_guard], key=lambda k: freq[best_guard][k])

    freq_guard, (freq_minute, _) = max(((gid, max(f.items(), key=lambda item: item[1]))
                                        for gid, f in freq.items()), key=lambda item: item[1][1])
    print(best_guard * most_asleep)
    print(freq_guard * freq_minute)


if __name__ == '__main__':
    main()
