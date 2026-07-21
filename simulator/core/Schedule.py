from Process import Process 
from PriorityQueue import PriorityQueue
from RoundRobinQueue import RoundRobinQueue
class Schedule:
    def __init__(self, quantum=2):
        self.priority_queue = PriorityQueue()
        self.round_robin_queue = RoundRobinQueue()
        self.process_storage = []
        self.gantt_history = []
        self.event_log = []
        self.clock = 0
        self.quantum = quantum
    def add_process(self, process_name,burst_time,process_type, priority):
        if process_name == "" or burst_time <= 0:
            print("Invalid Input")
            return
        
        new_process = Process(process_name,burst_time,process_type,priority)
        if process_type == "SYSTEM":
            self.priority_queue.enqueue(new_process)
        
        else:
           self.round_robin_queue.enqueue(new_process)
        self.process_storage.append(new_process)

    def round_robin_schedule(self):
        if self.round_robin_queue.is_empty():
            return None
        process = self.round_robin_queue.dequeue()
        process.remaining_time -= min(self.quantum,process.remaining_time)
        if process.remaining_time > 0:
            self.round_robin_queue.enqueue(process)
        return process
    
    def priority_schedule(self):
        if self.priority_queue.is_empty():
            return None
        process = self.priority_queue.dequeue()
        return process

    def execute_step(self):
        if not self.priority_queue.is_empty():
            process = self.priority_queue.dequeue()
        elif not self.round_robin_queue.is_empty():
            process = self.round_robin_queue.dequeue()
        else:
            return
        process.remaining_time -= 1
        self.gantt_history.append(process.name)
        if process.remaining_time == 0:
            process.finish(self.clock)
        else:
            if process.process_type == "SYSTEM":
                self.priority_queue.enqueue(process)
            else:
                self.round_robin_queue.enqueue(process)
        self.clock += 1
    
    def run_all(self):
        while (not self.priority_queue.is_empty() or not self.round_robin_queue.is_empty() ):
            self.execute_step()
    
    def render_gantt_chart(self):
        chart = []
        for record in self.gantt_history:
            if chart and chart[-1] == record:
                continue
            chart.append(record)
        return chart
    
    def calculate_statistics(self):
        total_turnaround = 0
        completed = 0
        for process in self.process_storage:
            if process.completed:
                total_turnaround += process.turnaround_time
                completed += 1
        if completed > 0:
            average_turnaround = (total_turnaround / completed)
        else:
            average_turnaround = 0
        completion_ratio = (completed / len(self.process_storage)) if self.process_storage else 0
        return (average_turnaround, completion_ratio, self.clock)

    def set_quantum(self, value):
        if value < 1:
            print("Invalid Quantum")
            return
        self.quantum = value
    
    def reset_simulation(self):
        self.round_robin_queue.clear()
        self.priority_queue.clear()
        self.process_storage.clear()
        self.event_log.clear()
        self.gantt_history.clear()
        self.clock = 0
    
    def add_log(self, message):
        self.event_log.append(message)
        if len(self.event_log) > 80:
            self.event_log.pop(0)





