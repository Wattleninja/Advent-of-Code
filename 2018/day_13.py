from enum import Enum
from itertools import cycle
from operator import itemgetter


class Direction(Enum):
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP = (0, -1)
    DOWN = (0, 1)


CART_DIRECTIONS = {
    '<': Direction.LEFT,
    '>': Direction.RIGHT,
    '^': Direction.UP,
    'v': Direction.DOWN
}

CART_DIRECTIONS_STR = {v: k for k, v in CART_DIRECTIONS.items()}

CART_TURN_DIRECTIONS = {
    '/': {
        Direction.LEFT: Direction.DOWN,
        Direction.RIGHT:  Direction.UP,
        Direction.UP:  Direction.RIGHT,
        Direction.DOWN:  Direction.LEFT
    },
    '\\': {
        Direction.LEFT: Direction.UP,
        Direction.RIGHT:  Direction.DOWN,
        Direction.UP:  Direction.LEFT,
        Direction.DOWN:  Direction.RIGHT
    }
}


INTERSECTION_CHOICES = (Direction.LEFT, None, Direction.RIGHT)
INTERSECTION_CHANGE_DIRECTIONS = {
    Direction.LEFT: {
        Direction.LEFT: Direction.DOWN,
        Direction.RIGHT:  Direction.UP,
        Direction.UP:  Direction.LEFT,
        Direction.DOWN:  Direction.RIGHT
    },
    Direction.RIGHT: {
        Direction.LEFT: Direction.UP,
        Direction.RIGHT:  Direction.DOWN,
        Direction.UP:  Direction.RIGHT,
        Direction.DOWN:  Direction.LEFT
    }
}


class Cart:
    def __init__(self, id_, x: int, y: int, direction: Direction):
        self.id = id_
        self.x = x
        self.y = y
        self.direction = direction
        self.crashed = False

        self.intersection_choices = cycle(INTERSECTION_CHOICES)

    @property
    def pos(self):
        return self.x, self.y

    def __lt__(self, other):
        return self.pos < other.pos

    def __eq__(self, other):
        return self.pos == other.pos

    def __repr__(self):
        return f'Cart#{self.id} @ {self.pos} {self.direction}'

    def move(self, track: dict, carts: list):
        dx, dy = self.direction.value
        self.x += dx
        self.y += dy

        pos = self.pos
        id_ = self.id
        for cart in carts:
            if cart.id == id_:
                continue

            if cart.pos == pos:
                return cart

        new_char = track.get((self.x, self.y))
        if new_char is None:
            return None

        if new_char in CART_TURN_DIRECTIONS:
            self.direction = CART_TURN_DIRECTIONS[new_char][self.direction]

        elif new_char == '+':
            intersection_choice = next(self.intersection_choices)
            if intersection_choice is not None:
                self.direction = INTERSECTION_CHANGE_DIRECTIONS[intersection_choice][self.direction]

        return None


def display_track(track, carts):
    width = max(track.keys(), key=itemgetter(0))[0] + 1
    height = max(track.keys(), key=itemgetter(1))[1] + 1
    cart_pos = {c.pos: CART_DIRECTIONS_STR[c.direction] for c in carts}

    print('\n'.join(''.join(cart_pos.get((x, y)) or track.get((x, y), ' ')
                            for x in range(width)) for y in range(height)))


def main():
    with open('inputs/13.in') as f:
        data = [line.rstrip() for line in f]

    track = {}
    carts = []

    for y, row in enumerate(data):
        for x, char in enumerate(row):
            if char == ' ':
                continue

            if char in CART_DIRECTIONS:
                cart = Cart(len(carts), x, y, CART_DIRECTIONS[char])
                carts.append(cart)
            # Include for display_track
            #     track[x, y] = '-' if cart.direction in (Direction.LEFT, Direction.RIGHT) else '|'
            # else:
            # elif char in ('+', '\\', '/'):
                track[x, y] = char

    while len(carts) > 1:
        carts.sort()
        # display_track(track, carts)
        for cart in carts:
            if cart.crashed:
                continue
            # print(cart)
            crashed_cart = cart.move(track, carts)
            if crashed_cart is not None:
                print(f'Crash {cart} and {crashed_cart}')
                cart.crashed = True
                crashed_cart.crashed = True

        carts = [cart for cart in carts if not cart.crashed]

    print(carts[0])


if __name__ == '__main__':
    main()
