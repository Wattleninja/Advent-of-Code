class Node:
    def __init__(self):
        self.metadata = []
        self.children = []

    @property
    def value(self):
        if not self.children:
            return sum(self.metadata)

        total = 0
        for i in self.metadata:
            i -= 1
            if i == -1 or i >= len(self.children):
                continue

            total += self.children[i].value
        return total


def parse_node(it):
    num_childs, num_metadata = next(it), next(it)
    node = Node()
    for _ in range(num_childs):
        child = parse_node(it)
        node.children.append(child)

    metadata = []
    for _ in range(num_metadata):
        metadata = next(it)
        node.metadata.append(metadata)

    return node


def metadata_sum(node: Node):
    total = sum(node.metadata)
    for child in node.children:
        total += metadata_sum(child)

    return total


def main():
    with open('08.in') as f:
        data = map(int, f.read().split())

    root = parse_node(data)
    print(metadata_sum(root))
    print(root.value)


if __name__ == '__main__':
    main()
