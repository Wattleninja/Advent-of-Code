def part_1(data):
    scoreboard = [3, 7]
    elves = [3, 7]
    elf_index = [0, 1]
    while len(scoreboard) < data:
        score = sum(elves)
        new_recipes = [int(i) for i in str(score)]
        scoreboard += new_recipes

        for index, (recipe, ei) in enumerate(zip(elves, elf_index)):
            recipe += ei + 1
            recipe %= len(scoreboard)
            elves[index] = scoreboard[recipe]
            elf_index[index] = recipe

    print(''.join(map(str, scoreboard[990941:])))


def part_2(data):
    data = list(map(int, str(data)))

    scoreboard = [3, 7]
    elves = [3, 7]
    current_indexs = [0, 1]
    while True:
        score = sum(elves)
        new_recipes = [int(i) for i in str(score)]
        scoreboard += new_recipes

        for index, (recipe, recipe_index) in enumerate(zip(elves, current_indexs)):
            recipe_index = (recipe_index + recipe + 1) % len(scoreboard)
            elves[index] = scoreboard[recipe_index]
            current_indexs[index] = recipe_index

        if scoreboard[-6:] == data or scoreboard[-7:-1] == data:
            break

    if scoreboard[-6:] == data:
        print(len(scoreboard) - 6)
    else:
        print(len(scoreboard) - 7)


def main():
    with open('inputs/14.in') as f:
        data = int(f.read())

    part_1(data + 10)
    part_2(data)


if __name__ == '__main__':
    main()
