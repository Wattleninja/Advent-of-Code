import itertools as it

from collections import deque
from operator import itemgetter

WALL = '#'
EMPTY = '.'
ELF_SYMBOL = 'E'
GOLBIN_SYMBOL = 'G'
DELTAS = ((0, -1), (-1, 0), (1, 0), (0, 1))


def sort_targets(unit):
    x, y = unit.pos
    return unit.hp, (y, x)


def sort_units(unit):
    x, y = unit.pos
    return y, x


class Unit:
    ally_symbol: str = None
    enemy_symbol: str = None

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.atk = 3
        self.hp = 200
        self.dead = False

    def __repr__(self):
        return f'{self.__class__.__name__}(x={self.x}, y={self.y}, hp={self.hp})'

    @property
    def pos(self):
        return self.x, self.y

    @pos.setter
    def pos(self, pos):
        self.x, self.y = pos

    def attack(self, unit: 'Unit'):
        return unit.take_damage(self.atk)

    def take_damage(self, damage: int):
        self.hp -= damage
        if self.hp <= 0:
            self.dead = True
        return self.dead

    def find_target(self, game: 'Game'):
        queue = deque([self.pos])
        seen = {self.pos}
        history = {self.pos: None}

        possible_targets = []
        steps = 0
        while queue:
            steps += 1
            pos = queue.popleft()
            for neighbour, char in game.get_neighbours(pos):
                if neighbour in seen:
                    continue

                if char == self.ally_symbol:
                    seen.add(neighbour)
                    continue

                elif char == self.enemy_symbol:
                    seen.add(neighbour)
                    history[neighbour] = pos
                    possible_targets.append(pos)
                    continue

                seen.add(neighbour)
                history[neighbour] = pos
                queue.append(neighbour)

            if possible_targets:
                possible_targets.sort(key=itemgetter(1, 0))
                move = possible_targets[0]

                while True:
                    prev = history[move]
                    if prev is None or history[prev] is None:
                        if game[move] != EMPTY:  # self.pos == move | same case
                            return None
                        return move
                    move = prev

    def get_target(self, game: 'Game'):
        targets_pos = set()
        for neighbour, char in game.get_neighbours(self.pos):
            if char == self.enemy_symbol:
                targets_pos.add(neighbour)

        if not targets_pos:
            return None

        targets = [t for t in self.get_enemies(game) if t.pos in targets_pos and not t.dead]
        targets.sort(key=sort_targets)
        return targets[0]

    def get_enemies(self, game: 'Game'):
        raise NotImplementedError


class Elf(Unit):
    ally_symbol = ELF_SYMBOL
    enemy_symbol = GOLBIN_SYMBOL

    def get_enemies(self, game: 'Game'):
        return game.goblins


class Goblin(Unit):
    ally_symbol = GOLBIN_SYMBOL
    enemy_symbol = ELF_SYMBOL

    def get_enemies(self, game: 'Game'):
        return game.elves


class Game:
    def __init__(self, grid, elves, goblins):
        self.grid = grid
        self.elves = elves
        self.goblins = goblins
        self.width = len(self.grid[0])
        self.height = len(self.grid)
        self.rounds = 0

    def __getitem__(self, pos):
        x, y = pos
        return self.grid[y][x]

    def __setitem__(self, pos, value):
        x, y = pos
        self.grid[y][x] = value

    def __str__(self):
        text = f'Rounds={self.rounds} Elves={len(self.elves)} Golbins={len(self.goblins)}\n'
        units = sorted(it.chain(self.elves, self.goblins), key=sort_units)

        for y, row in enumerate(self.grid):
            text += ''.join(row) + '\t'
            text += ' '.join(repr(u) for u in units if u.y == y)
            text += '\n'

        return text

    def move_unit(self, unit, pos):
        self[unit.pos] = EMPTY
        unit.pos = pos
        self[pos] = unit.ally_symbol

    @classmethod
    def from_file(cls, filename) -> 'Game':
        grid = []
        elves = []
        goblins = []
        with open(filename) as f:
            for y, line in enumerate(f):
                row = []
                line = line.rstrip()
                for x, char in enumerate(line):
                    row.append(char)
                    if char == ELF_SYMBOL:
                        elves.append(Elf(x, y))
                    elif char == GOLBIN_SYMBOL:
                        goblins.append(Goblin(x, y))
                grid.append(row)
        return cls(grid, elves, goblins)

    def get_neighbours(self, pos):
        x, y = pos
        for dx, dy in DELTAS:
            x2 = x + dx
            y2 = y + dy
            if not (0 <= x2 < self.width and 0 <= y2 < self.height):
                continue

            char = self.grid[y2][x2]
            if char != WALL:
                yield (x2, y2), char

    def run(self):
        while self.elves and self.goblins:
            units = sorted(it.chain(self.elves, self.goblins), key=sort_units)
            for unit in units:
                unit: Unit
                if unit.dead:
                    continue

                new_pos = unit.find_target(self)
                if new_pos is not None:
                    self.move_unit(unit, new_pos)

                enemy = unit.get_target(self)
                if enemy is not None:
                    if unit.attack(enemy):
                        self[enemy.pos] = EMPTY
                        self.elves = [e for e in self.elves if not e.dead]
                        self.goblins = [g for g in self.goblins if not g.dead]

                if not (self.elves and self.goblins):
                    break
            else:
                self.rounds += 1

            print(self)

        return self.rounds * sum(u.hp for u in it.chain(self.elves, self.goblins))


def main():
    game: Game = Game.from_file('inputs/15.in')
    print(game)
    print(game.run())
    print(game)


if __name__ == '__main__':
    main()
    # import sys
    # with open('15.out', 'w') as stdf:
    #     stdout_ = sys.stdout
    #     sys.stdout = stdf
    #     main()
    #     sys.stdout = stdout_
