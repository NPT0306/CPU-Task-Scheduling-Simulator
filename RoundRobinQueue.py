class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class RoundRobinQueue:
    """Custom FIFO queue implemented with a singly linked list.
    enqueue: O(1) — append at tail
    dequeue: O(1) — remove from head
    """

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def enqueue(self, process):
        new_node = Node(process)
        if self.tail is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def dequeue(self):
        if self.head is None:
            raise IndexError("dequeue from empty queue")
        node = self.head
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self.size -= 1
        return node.value

    def is_empty(self):
        return self.size == 0

    def clear(self):
        self.head = None
        self.tail = None
        self.size = 0