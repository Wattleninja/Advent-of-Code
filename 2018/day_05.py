from string import ascii_lowercase


def react(s):
    stack = []
    for char in s:
        if stack and stack[-1] == char.swapcase():
            stack.pop()
        else:
            stack.append(char)
    return ''.join(stack)


def main():
    with open('05.in') as f:
        data = f.read().strip()

    print(len(react(data)))

    reacts = []
    for char in ascii_lowercase:
        s = react(data.translate(str.maketrans('', '', char + char.upper())))
        reacts.append(len(s))

    print(min(reacts))


if __name__ == '__main__':
    main()
