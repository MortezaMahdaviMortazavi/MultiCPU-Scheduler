import threading
import time
import random
from queue import Queue
from process import Process , ProcessHybrid

class ScoreTracker:
    def __init__(self):
        self.total_score = 0
        self.missed_processes = 0
        self.lock = threading.Lock()
    
    def add_score(self, value: int):
        with self.lock:
            self.total_score += value
    
    def add_missed(self):
        with self.lock:
            self.missed_processes += 1

class ProcessGenerator(threading.Thread):
    def __init__(self, output_queue: Queue, max_processes=50):
        super().__init__()
        self.output_queue = output_queue
        self.process_count = 0
        self.max_processes = max_processes
        self._stop_event = threading.Event()
        self.process_list = []  # Store generated processes

    def generate_process(self) -> Process:
        current_time = time.time()
        return Process(
            id=self.process_count,
            arrival_time=current_time,
            execution_time=random.uniform(0.5,2.0),  # Increased max execution time
            starting_deadline=current_time + random.uniform(0.5, 2.0),  # Tighter deadlines
            ending_deadline=current_time + random.uniform(1.7, 2.5),
            value=random.randint(1, 100)
        )

    def run(self):
        while not self._stop_event.is_set() and self.process_count < self.max_processes:
            process = self.generate_process()
            self.output_queue.put(process)
            self.process_count += 1
            self.process_list.append(process)
            time.sleep(random.uniform(0.2,0.4))  # More varied generation intervals
        
        self.output_queue.put(None)

    def stop(self):
        self._stop_event.set()