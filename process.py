import random
from dataclasses import dataclass
from typing import Optional


@dataclass
class Process:
    id: int
    arrivalTime: int
    executionTime: int
    startingDeadline: int
    endingDeadline: int
    value: int

    def get_remaining_time(self, current_time: int) -> int:
        return self.endingDeadline - current_time

    def is_expired(self, current_time: int) -> bool:
        return current_time > self.startingDeadline or current_time > self.endingDeadline

    def __str__(self) -> str:
        return (f"Process(id={self.id}, arrivalTime={self.arrivalTime}, "
                f"executionTime={self.executionTime}, startingDeadline={self.startingDeadline}, "
                f"endingDeadline={self.endingDeadline}, value={self.value})")



class ProcessGenerator:
    def __init__(self, max_count: Optional[int] = None):
        self.process_count = 0
        self.max_count = max_count if max_count is not None else 100
        self.random = random.Random()

    def generate_process(self) -> Process:
        arrival_time = self.process_count  # Sequential arrival time for simplicity
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
            yield process