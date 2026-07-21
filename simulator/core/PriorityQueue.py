class PriorityQueue:
    """Custom min-heap implemented on a plain Python list (array).
    enqueue (push): O(log n)
    dequeue (pop):  O(log n)
    Lower priority value = higher priority (served first).
    """

    def __init__(self):
        self.heap = []  # each element: (priority, counter, process)
        self._counter = 0  # tiebreaker to avoid comparing Process objects directly

    def enqueue(self, process):
        entry = (process.priority, self._counter, process)
        self._counter += 1
        self.heap.append(entry)
        self._sift_up(len(self.heap) - 1)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from empty priority queue")
        top = self.heap[0]
        last = self.heap.pop()
        if self.heap:
            self.heap[0] = last
            self._sift_down(0)
        return top[2]  # return the process object

    def is_empty(self):
        return len(self.heap) == 0

    def clear(self):
        self.heap = []
        self._counter = 0

    # ---- internal heap helpers ----
    def _sift_up(self, index):
        parent = (index - 1) // 2
        while index > 0 and self.heap[index] < self.heap[parent]:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            index = parent
            parent = (index - 1) // 2

    def _sift_down(self, index):
        size = len(self.heap)
        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            smallest = index

            if left < size and self.heap[left] < self.heap[smallest]:
                smallest = left
            if right < size and self.heap[right] < self.heap[smallest]:
                smallest = right
            if smallest == index:
                break

            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            index = smallest