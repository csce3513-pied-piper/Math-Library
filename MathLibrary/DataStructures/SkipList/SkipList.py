from random import randint, seed


class Node:
    def __init__(self, height=0, elem=None):
        self.elem = elem
        self.next = [None] * height


def random_height():
    height = 1
    while randint(1, 2) != 1:
        height += 1
    return height


class SkipList:

    def __init__(self):
        self.head = Node()
        self.len = 0
        self.maxHeight = 0

    def __len__(self):
        return self.len

    def find(self, elem, update=None):
        if update is None:
            self.update_list(elem)
        elif len(update) > 0:
            item = update[0].next[0]
            if item is not None and item.elem == elem:
                return item
        return None

    def contains(self, elem, update=None):
        return self.find(elem, update) is not None

    def update_list(self, elem):
        update = [None] * self.maxHeight
        x = self.head
        for i in reversed(range(self.maxHeight)):
            while x.next[i] is not None and x.next[i].elem < elem:
                x = x.next[i]
            update[i] = x
        return update

    def insert(self, elem):

        _node = Node(random_height(), elem)

        self.maxHeight = max(self.maxHeight, len(_node.next))
        while len(self.head.next) < len(_node.next):
            self.head.next.append(None)

        update = self.update_list(elem)
        if self.find(elem, update) is None:
            for i in range(len(_node.next)):
                _node.next[i] = update[i].next[i]
                update[i].next[i] = _node
            self.len += 1

    def remove(self, elem):

        update = self.update_list(elem)
        x = self.find(elem, update)
        if x is not None:
            for i in reversed(range(len(x.next))):
                update[i].next[i] = x.next[i]
                if self.head.next[i] is None:
                    self.maxHeight -= 1
            self.len -= 1

    def print_list(self):
        for i in range(len(self.head.next) - 1, -1, -1):
            x = self.head
            while x.next[i] is not None:
                print(x.next[i].elem)
                x = x.next[i]
            print('')
