from collections import deque
import heapq

class Process:
    def __init__(self, name, burst_time, process_type, priority=0):
        self.name = name
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.process_type = process_type
        self.priority = priority
        self.arrival_time = 0
        self.finish_time = None
        self.completed = False
    def run_one_tick(self):
        self.remaining_time -= 1
    def is_finished(self):
        return self.remaining_time <= 0
    
class RoundRobinQueue:
    def __init__(self):
        self.queue = deque()
    def enqueue(self, process):
        self.queue.append(process)
    def dequeue(self):
        return self.queue.popleft()
    def is_empty(self):
        return len(self.queue) == 0
    
class PriorityQueue:
    def __init__(self):
        self.heap = []
    def enqueue(self, process):
        heapq.heappush(
            self.heap,
            (process.priority, process)
        )
    def dequeue(self):
        return heapq.heappop(self.heap)[1]
    def is_empty(self):
        return len(self.heap) == 0
