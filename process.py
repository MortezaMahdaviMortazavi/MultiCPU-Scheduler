import random
import time
import threading
from dataclasses import dataclass
from typing import Optional
from queue import Queue

@dataclass
class Process:
    id: int
    arrival_time: int
    execution_time: int
    starting_deadline: int
    ending_deadline: int
    value: int

    def get_remaining_time(self, current_time: int) -> int:
        return self.ending_deadline - current_time

    def is_expired(self, current_time: int) -> bool:
        return current_time > self.starting_deadline or current_time > self.ending_deadline

    def __str__(self) -> str:
        return (f"Process(id={self.id}, arrival_time={self.arrival_time}, "
                f"execution_time={self.execution_time}, starting_deadline={self.starting_deadline}, "
                f"ending_deadline={self.ending_deadline}, value={self.value})")


class ProcessGenerator:
    def __init__(self, max_count: Optional[int] = None):
        self.process_count = 0
        self.max_count = max_count if max_count is not None else 100
        self.random = random.Random()
        self.processes_queue = Queue()  # Thread-safe queue

    def generate_process(self) -> Process:
        arrival_time = int(time.time())  # Use current timestamp for real-time arrival
        execution_time = self.random.randint(1, 10)
        starting_deadline = arrival_time + self.random.randint(1, 5)
        ending_deadline = starting_deadline + execution_time + self.random.randint(1, 5)
        value = self.random.randint(1, 100)
        
        process = Process(
            id=self.process_count,
            arrival_time=arrival_time,
            execution_time=execution_time,
            starting_deadline=starting_deadline,
            ending_deadline=ending_deadline,
            value=value
        )
        
        self.process_count += 1
        return process

    def run(self):
        while self.process_count < self.max_count:
            process = self.generate_process()
            self.processes_queue.put(process)  # Add process to the thread-safe queue
            print(f"Generated: {process}")
            time.sleep(self.random.uniform(0.5, 2.0))  # Random delay between process generation



# Reinfrocement learning base scheduling
