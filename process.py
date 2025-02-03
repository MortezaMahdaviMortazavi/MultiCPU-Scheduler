import random
import time
import threading
from dataclasses import dataclass
from typing import Optional
from queue import Queue

@dataclass
class Process:
    id: int
    arrival_time: float
    execution_time: float
    starting_deadline: float
    ending_deadline: float
    value: int
    missed_deadline: bool = False

    def is_expired(self, current_time: float) -> bool:
        return current_time > self.starting_deadline

    def can_finish(self, current_time: float) -> bool:
        return current_time + self.execution_time <= self.ending_deadline

    def __lt__(self, other):
        # Composite priority: Value > Deadline > Execution Time
        if self.value != other.value:
            return self.value > other.value
        if self.starting_deadline != other.starting_deadline:
            return self.starting_deadline < other.starting_deadline
        return self.execution_time < other.execution_time
    
    def __repr__(self):
        return (
            f"Process(id={self.id}, missed_deadline={self.missed_deadline})"
        )





@dataclass
class ProcessHybrid(Process):
    def __lt__(self, other):
        """
        Hybrid composite ordering:

        - First, reward a high value per unit of execution time.
        - Second, reward processes with tighter deadlines (lower slack).
        
        The slack time is defined as:
            slack = ending_deadline - arrival_time - execution_time
        A lower slack means the process must be run sooner to meet its deadline.
        
        We compute a composite score for each process. A higher score indicates a more attractive process.
        Since heapq in Python is a min-heap, we define __lt__ such that the process with
        the higher composite score is considered "greater".
        """
        slack_self = max(self.ending_deadline - self.arrival_time - self.execution_time, 0.001)
        slack_other = max(other.ending_deadline - other.arrival_time - other.execution_time, 0.001)
        
        base_self = self.value / self.execution_time
        base_other = other.value / other.execution_time

        urgency_self = 1 / slack_self
        urgency_other = 1 / slack_other

        weight_base = 1.0
        weight_urgency = 1.0

        score_self = weight_base * base_self + weight_urgency * urgency_self
        score_other = weight_base * base_other + weight_urgency * urgency_other

        return score_self < score_other



