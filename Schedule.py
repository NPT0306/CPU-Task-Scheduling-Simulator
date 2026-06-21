import Process 
class Schedule:
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
