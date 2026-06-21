class Process:
    def __init__(self, name, burst_time, process_type, priority=0):
        self.name = name
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.process_type = process_type
        self.priority = priority
        self.arrival_time = 0
        self.finish_time = None
        self.turnaround_time = None
        self.completed = False

    def run_one_tick(self):
        self.remaining_time -= 1

    def is_finished(self):
        return self.remaining_time <= 0

    def finish(self, current_time):
        """Gọi khi process hoàn thành để chốt finish_time và turnaround_time."""
        self.finish_time = current_time
        self.turnaround_time = self.finish_time - self.arrival_time
        self.completed = True