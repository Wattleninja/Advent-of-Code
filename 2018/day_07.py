from collections import defaultdict, deque
from bisect import insort


def main():
    waiting = defaultdict(list)
    steps = set()
    num_workers = 5
    step_delay = 60

    with open('07.in') as f:
        for line in f:
            parts = line.strip().split()
            req_step, step = parts[1], parts[7]

            waiting[step].append(req_step)
            steps.add(req_step)
            steps.add(step)

    available = deque(sorted(steps.difference(waiting.keys())))

    part_1(waiting.copy(), steps.copy(), available.copy())
    part_2(waiting.copy(), steps.copy(), available.copy(),
           num_workers, step_delay)


def part_1(waiting: dict, steps: set, available: deque):
    order = ''
    completed = set()

    while len(completed) < len(steps):
        if available:
            step = available.popleft()
            completed.add(step)
            order += step

        for step, reqs in list(waiting.items()):
            if all(req in completed for req in reqs):
                insort(available, step)
                waiting.pop(step)

    print(order)


def part_2(waiting: dict, steps: set, available: deque, num_workers, step_delay):
    time_taken = 0
    completed = set()
    workers = defaultdict(int)
    offset = -ord('A') + 1 + step_delay

    for _ in range(num_workers):
        if not available:
            break
        step = available.popleft()
        workers[step] = ord(step) + offset

    while len(completed) < len(steps):
        for step in workers.copy():
            workers[step] -= 1
            if workers[step] == 0:
                completed.add(step)
                workers.pop(step)

        for step, reqs in list(waiting.items()):
            if all(req in completed for req in reqs):
                insort(available, step)
                waiting.pop(step)

        for _ in range(num_workers - len(workers)):
            if not available:
                break
            step = available.popleft()
            workers[step] = ord(step) + offset

        time_taken += 1

    print(time_taken)


if __name__ == '__main__':
    main()
